from rest_framework import serializers

from app.pastor_history.models import PastorHistory


class PastorHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PastorHistory
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
