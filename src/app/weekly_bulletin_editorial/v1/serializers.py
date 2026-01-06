from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial
from app.weekly_bulletin_editorial.v1.nested_serializers import WeeklyBulletinEditorialFileSerializer


class WeeklyBulletinEditorialSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    file_set = WeeklyBulletinEditorialFileSerializer(label="파일", many=True)

    class Meta:
        model = WeeklyBulletinEditorial
        fields = [
            "id",
            "user",
            "title",
            "body",
            "file_set",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
