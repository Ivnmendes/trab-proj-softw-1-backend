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
            "description",
            "concentration",
            "components",
            "cids",
            "documents",
            "pharmacies",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
