from rest_framework import serializers

from app.passing_notice.models import PassingNotice


class PassingNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassingNotice
        fields = [
            "id",
            "portrait",
            "name",
            "baptismal_name",
            "passing_at",
            "funeral_start_at",
            "funeral_end_at",
            "funeral_hall_address",
            "encoffinment_at",
            "departure_at",
        ]
