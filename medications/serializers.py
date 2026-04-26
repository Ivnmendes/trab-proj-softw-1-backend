from rest_framework import serializers

from map.serializers import PharmacySerializer

from .models import CID, Document, Medication


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class CIDSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = CID
        fields = [
            "id",
            "name",
            "description",
            "code",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class MedicationSerializer(serializers.ModelSerializer):
    cids = CIDSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    pharmacies = PharmacySerializer(many=True, read_only=True)

    class Meta:
        model = Medication
        fields = [
            "id",
            "generic_name",
            "name",
            "type",
            "description",
            "concentration",
            "cids",
            "documents",
            "pharmacies",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class MedicationPublicSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField()
    principioAtivo = serializers.CharField(source="generic_name", read_only=True)
    apresentacao = serializers.CharField(source="concentration", read_only=True)
    disponivel = serializers.SerializerMethodField()
    unidadeSaude = serializers.SerializerMethodField()
    descricao = serializers.CharField(source="description", read_only=True)
    tipo = serializers.CharField(source="type", read_only=True)
    farmacias = PharmacySerializer(source="pharmacies", many=True, read_only=True)
    cids = CIDSerializer(many=True, read_only=True)
    documentos = DocumentSerializer(source="documents", many=True, read_only=True)

    class Meta:
        model = Medication
        fields = [
            "id",
            "nome",
            "principioAtivo",
            "apresentacao",
            "disponivel",
            "unidadeSaude",
            "descricao",
            "tipo",
            "farmacias",
            "cids",
            "documentos",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields

    def get_nome(self, obj):
        if obj.name and obj.concentration:
            return f"{obj.name} {obj.concentration}"
        if obj.name:
            return obj.name
        if obj.concentration:
            return f"{obj.generic_name} {obj.concentration}"
        return obj.generic_name

    def get_disponivel(self, obj):
        return True

    def get_unidadeSaude(self, obj):
        pharmacies = list(obj.pharmacies.all())
        if not pharmacies:
            return "Sem estoque no momento"
        if len(pharmacies) == 1:
            return pharmacies[0].name
        return [pharmacy.name for pharmacy in pharmacies]
