from rest_framework import serializers

from app.priest.models import Priest


class PriestSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = Priest
        fields = [
            "id",
            "image",
            "name",
            "baptismal_name",
            "ordination_date",
            "is_retired",
            "role_display",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]


class PastorSerializer(PriestSerializer):
    class Meta(PriestSerializer.Meta):
        fields = PriestSerializer.Meta.fields + [
            "division",
            "start_date",
            "end_date",
        ]


class AssociateSerializer(PastorSerializer):
    class Meta(PastorSerializer.Meta):
        fields = PastorSerializer.Meta.fields + [
            "assistant_system",
        ]
