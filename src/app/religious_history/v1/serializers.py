from rest_framework import serializers

from app.religious_history.models import ReligiousHistory


class ReligiousHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligiousHistory
        fields = [
            "id",
            "category",
            "name",
            "baptismal_name",
            "start_date",
            "end_date",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]
