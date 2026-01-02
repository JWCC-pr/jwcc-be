from rest_framework import serializers

from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial
from app.weekly_bulletin_editorial.v1.nested_serializers import WeeklyBulletinEditorialFileSerializer


class WeeklyBulletinEditorialSerializer(serializers.ModelSerializer):
    file_set = WeeklyBulletinEditorialFileSerializer(label="파일", many=True)

    class Meta:
        model = WeeklyBulletinEditorial
        fields = [
            "id",
            "title",
            "body",
            "file_set",
            "created_at",
            "updated_at",
        ]
