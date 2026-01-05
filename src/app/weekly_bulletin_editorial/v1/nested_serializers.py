from rest_framework import serializers

from app.weekly_bulletin_editorial_file.models import WeeklyBulletinEditorialFile


class WeeklyBulletinEditorialFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyBulletinEditorialFile
        fields = [
            "file",
        ]
        ref_name = "WeeklyBulletinEditorialFileSerializer"
