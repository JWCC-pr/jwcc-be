from rest_framework import serializers

from app.department_board_image.models import DepartmentBoardImage


class DepartmentBoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentBoardImage
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
