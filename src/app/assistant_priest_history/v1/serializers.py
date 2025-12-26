from rest_framework import serializers

from app.assistant_priest_history.models import AssistantPriestHistory


class AssistantPriestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssistantPriestHistory
        fields = [
            "id",
            "assistant_system",
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
