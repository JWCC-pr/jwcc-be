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
            "age",
            "passing_at",
            "funeral_start_at",
            "funeral_end_at",
            "funeral_mass_at",
            "funeral_mass_location",
            "funeral_hall_address",
            "chief_mourner",
            "encoffinment_at",
            "departure_at",
            "comment_count",
            "created_at",
        ]
