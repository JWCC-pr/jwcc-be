from rest_framework import serializers

from app.weekly_bulletin_request.models import WeeklyBulletinRequest


class WeeklyBulletinRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBulletinRequest
        fields = [
            "id",
            "title",
            "file",
        ]
