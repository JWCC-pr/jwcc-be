from django.db import transaction
from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial
from app.weekly_bulletin_editorial.v1.nested_serializers import WeeklyBulletinEditorialFileSerializer
from app.weekly_bulletin_editorial_file.models import WeeklyBulletinEditorialFile


class WeeklyBulletinEditorialSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    file_set = WeeklyBulletinEditorialFileSerializer(
        label="파일",
        many=True,
        required=False,
        allow_empty=True,
    )

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
        with transaction.atomic():
            file_data_set = validated_data.pop("file_set", [])
            validated_data["user"] = self.context["request"].user

            editorial = WeeklyBulletinEditorial.objects.create(**validated_data)

            if file_data_set:
                WeeklyBulletinEditorialFile.objects.bulk_create(
                    [
                        WeeklyBulletinEditorialFile(
                            weekly_bulletin_editorial=editorial,
                            **file_data,
                        )
                        for file_data in file_data_set
                    ]
                )
        return editorial

    def update(self, instance, validated_data):
        with transaction.atomic():
            file_data_set = validated_data.pop("file_set", None)

            editorial = super().update(instance, validated_data)

            if file_data_set is not None:
                editorial.file_set.all().delete()
                if file_data_set:
                    WeeklyBulletinEditorialFile.objects.bulk_create(
                        [
                            WeeklyBulletinEditorialFile(
                                weekly_bulletin_editorial=editorial,
                                **file_data,
                            )
                            for file_data in file_data_set
                        ]
                    )
        return editorial
