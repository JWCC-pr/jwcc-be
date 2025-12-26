from rest_framework import serializers

from app.priest_history.models import PriestHistory


class PriestHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PriestHistory
        fields = [
            "id",
            "name",
            "baptismal_name",
            "ordination_date",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]
