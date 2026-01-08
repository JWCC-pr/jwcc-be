from rest_framework import serializers

from app.weekly_bulletin_editorial_file.models import WeeklyBulletinEditorialFile


class WeeklyBulletinEditorialFileSerializer(serializers.ModelSerializer):
    file = serializers.URLField(label="파일")

    class Meta:
        model = WeeklyBulletinEditorialFile
        fields = [
            "id",
            "file",
        ]
        ref_name = "WeeklyBulletinEditorialFileSerializer"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["file"] = instance.file.url
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["file"] = ret["file"].replace(WeeklyBulletinEditorialFile._meta.get_field("file").storage.url(""), "")
        return ret
