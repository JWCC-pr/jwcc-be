from rest_framework import serializers

from app.religious.models import Religious


class ReligiousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religious
        fields = [
            "id",
            "image",
            "category",
            "name",
            "baptismal_name",
            "start_date",
            "is_retired",
            "end_date",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]
