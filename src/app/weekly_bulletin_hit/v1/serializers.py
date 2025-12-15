from rest_framework import serializers

from app.weekly_bulletin_hit.models import WeeklyBulletinHit


class WeeklyBulletinHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBulletinHit
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
