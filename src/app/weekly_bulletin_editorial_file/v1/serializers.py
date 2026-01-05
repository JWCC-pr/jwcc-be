from rest_framework import serializers

from app.weekly_bulletin_editorial_file.models import WeeklyBulletinEditorialFile


class WeeklyBulletinEditorialFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBulletinEditorialFile
        fields = [
            "id",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance
