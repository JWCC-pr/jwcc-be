from rest_framework import serializers

from app.weekly_bulletin_request.models import WeeklyBulletinRequest


class WeeklyBulletinRequestSerializer(serializers.ModelSerializer):
    file = serializers.URLField(label="파일")

    class Meta:
        model = WeeklyBulletinRequest
        fields = [
            "id",
            "title",
            "file",
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["file"] = ret["file"].replace(WeeklyBulletinRequest._meta.get_field("file").storage.url(""), "")
        return ret

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["file"] = instance.file.url
        return ret
