from rest_framework import serializers
from core.models import Drug


class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = [
            "id",
            "name",
            "dosage",
            "batch_number",
            "manufacture_date",
            "expiry_date",
            "manufacturer",
            "unique_code",
        ]
