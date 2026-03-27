from rest_framework import serializers

from .models import Landmark, Pharmacy


class LandmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landmark
        fields = [
            "id",
            "name",
            "description",
            "latitude",
            "longitude",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class PharmacySerializer(serializers.ModelSerializer):
    landmark = LandmarkSerializer(read_only=True)

    class Meta:
        model = Pharmacy
        fields = [
            "id",
            "name",
            "description",
            "type",
            "address",
            "landmark",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
