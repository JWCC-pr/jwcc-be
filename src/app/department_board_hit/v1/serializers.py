from rest_framework import serializers

from app.department_board_hit.models import DepartmentBoardHit


class DepartmentBoardHitSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentBoardHit
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
