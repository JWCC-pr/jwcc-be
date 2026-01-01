from django.db import transaction
from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.department_board.models import DepartmentBoard
from app.department_board_image.models import DepartmentBoardImage
from app.department_board_image.v1.serializers import DepartmentBoardImageSerializer


class DepartmentBoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)
    image_set = DepartmentBoardImageSerializer(label="이미지", many=True)

    class Meta:
        model = DepartmentBoard
        fields = [
            "id",
            "user",
            "title",
            "body",
            "image_set",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
            "is_modified",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set")
            validated_data["user"] = self.context["request"].user
            department_board = DepartmentBoard.objects.create(**validated_data)
            DepartmentBoardImage.objects.bulk_create(
                [
                    DepartmentBoardImage(
                        department_board=department_board,
                        **image_data,
                    )
                    for image_data in image_data_set
                ]
            )
        return department_board

    def update(self, instance, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set")
            department_board = super().update(instance, validated_data)
            department_board.image_set.all().delete()
            DepartmentBoardImage.objects.bulk_create(
                [
                    DepartmentBoardImage(
                        department_board=department_board,
                        **image_data,
                    )
                    for image_data in image_data_set
                ]
            )
        return instance
        validated_data["is_modified"] = True
        instance = super().update(instance, validated_data)
        return instance
