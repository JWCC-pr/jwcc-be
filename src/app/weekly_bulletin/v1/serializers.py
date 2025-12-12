from rest_framework import serializers

from app.weekly_bulletin.models import WeeklyBulletin


class WeeklyBulletinSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBulletin
        fields = [
            "id",
            "thumbnail",
            "title",
            "file",
        ]

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance
