from rest_framework import serializers

from app.religious.models import Religious


class ReligiousSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religious
        fields = [
            "id",
            "image",
            "category",
            "name",
            "baptismal_name",
            "start_date",
            "is_retired",
            "end_date",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["order"]

    def validate(self, attrs):
        is_retired = attrs.get("is_retired", getattr(self.instance, "is_retired", False))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if is_retired and not end_date:
            raise serializers.ValidationError({"end_date": "퇴임 시 재임 종료일을 입력해야 합니다."})

        return attrs
