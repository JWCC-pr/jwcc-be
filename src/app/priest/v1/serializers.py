from rest_framework import serializers
from app.priest.models import Priest


class PriestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Priest
        fields = [
            "id",
            "image",
            "name",
            "baptismal_name",
            "ordination_date",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]
