import csv
import io

from django.db import transaction

from medications.models import Medication
from map.models import Pharmacy

def import_medications_service(file):
    try:
        file.seek(0)
        file_data = io.TextIOWrapper(file, encoding='utf-8-sig')
        
        primeira_linha = file_data.readline()
        if not primeira_linha.startswith("Medicamentos e Fórmulas"):
            file_data.seek(0)
        
        reader = csv.DictReader(file_data, delimiter=';')
        
        pharmacys_map = {name.lower(): id for name, id in Pharmacy.objects.values_list('name', 'id')}
        specialized_id = pharmacys_map.get("farmácia de medicamentos especiais")

        medications_dict = {}

        for row in reader:
            nome_med = row['Nome'].strip().capitalize()
            concentracao = row['Concentração'].strip()
            
            chave = (nome_med, concentracao)

            if chave not in medications_dict:
                medications_dict[chave] = {
                    'med': Medication(generic_name=nome_med, concentration=concentracao),
                    'pharmacies': set()
                }

            names = [item.strip().lower() for item in row['Postos de Distribuição'].split('•') if item.strip()]
            components = set(row["Componente"].replace(" e ", " ").split())
            
            found_ids = [pharmacys_map[n] for n in names if n in pharmacys_map]
            
            if "Especializado" in components and specialized_id:
                found_ids.append(specialized_id)
            
            medications_dict[chave]['pharmacies'].update(found_ids)

        with transaction.atomic():
            meds_to_create = [data['med'] for data in medications_dict.values()]
            created_meds = Medication.objects.bulk_create(meds_to_create)

            MedicationPharmacyRel = Medication.pharmacies.through
            relations_to_create = []

            for med_obj, data in zip(created_meds, medications_dict.values()):
                for p_id in data['pharmacies']:
                    relations_to_create.append(
                        MedicationPharmacyRel(medication_id=med_obj.id, pharmacy_id=p_id)
                    )

            MedicationPharmacyRel.objects.bulk_create(relations_to_create)

        return (None, True)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return (e, False)