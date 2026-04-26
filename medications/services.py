import csv
import io
from django.db import transaction

from medications.models import Medication, CID, Document
from map.models import Pharmacy

def import_medications_service(file):
    try:
        file.seek(0)
        file_data = io.TextIOWrapper(file, encoding='utf-8-sig')
        
        first_line = file_data.readline()
        if not first_line.startswith("Medicamentos e Fórmulas"):
            file_data.seek(0)
        
        reader = csv.DictReader(file_data, delimiter=';')
        
        pharmacys_map = {name.lower(): id for name, id in Pharmacy.objects.values_list('name', 'id')}
        specialized_id = pharmacys_map.get("farmácia de medicamentos especiais")

        medications_dict = {}

        for row in reader:
            med_name = row['Nome'].strip().capitalize()
            concentration = row['Concentração'].strip()
            components = set(row["Componente"].replace(" e ", " ").split())
            
            key = (med_name, concentration)

            if key not in medications_dict:
                medications_dict[key] = {
                    'med': Medication(
                        generic_name=med_name, 
                        concentration=concentration,
                        type=Medication.MedicationType.SPECIALIZED if "Especializado" in components else Medication.MedicationType.BASIC
                    ),
                    'pharmacies': set()
                }

            names = [item.strip().lower() for item in row['Postos de Distribuição'].split('•') if item.strip()]
            
            found_ids = [pharmacys_map[n] for n in names if n in pharmacys_map]
            
            if "Especializado" in components and specialized_id:
                found_ids.append(specialized_id)
            
            medications_dict[key]['pharmacies'].update(found_ids)

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