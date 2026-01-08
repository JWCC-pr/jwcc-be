from django.db import transaction
from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.department_board.models import DepartmentBoard
from app.department_board.v1.nested_serializers import DepartmentBoardFileSerializer, DepartmentBoardImageSerializer
from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage


class DepartmentBoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)
    image_set = DepartmentBoardImageSerializer(
        label="이미지",
        many=True,
        required=False,
        allow_empty=True,
    )
    file_set = DepartmentBoardFileSerializer(
        label="파일",
        many=True,
        required=False,
        allow_empty=True,
    )

    class Meta:
        model = DepartmentBoard
        fields = [
            "id",
            "user",
            "department",
            "sub_department",
            "title",
            "body",
            "image_set",
            "file_set",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
            "is_modified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["department"]

    def validate_sub_department(self, value):
        user = self.context["request"].user
        user_sub_department_ids = user.sub_department_set.values_list("id", flat=True)
        if value.id not in user_sub_department_ids:
            raise serializers.ValidationError("소속된 세부분과만 선택할 수 있습니다.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            image_data_set = validated_data.pop("image_set", [])
            file_data_set = validated_data.pop("file_set", [])
            user = self.context["request"].user
            validated_data["user"] = user
            validated_data["department"] = validated_data["sub_department"].department

            department_board = DepartmentBoard.objects.create(**validated_data)

            if image_data_set:
                DepartmentBoardImage.objects.bulk_create(
                    [
                        DepartmentBoardImage(
                            department_board=department_board,
                            **image_data,
                        )
                        for image_data in image_data_set
                    ]
                )

            if file_data_set:
                DepartmentBoardFile.objects.bulk_create(
                    [
                        DepartmentBoardFile(
                            department_board=department_board,
                            **file_data,
                        )
                        for file_data in file_data_set
                    ]
                )
        return department_board

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data["is_modified"] = True
            image_data_set = validated_data.pop("image_set", None)
            file_data_set = validated_data.pop("file_set", None)

            if "sub_department" in validated_data:
                validated_data["department"] = validated_data["sub_department"].department

            department_board = super().update(instance, validated_data)

            # 이미지가 명시적으로 전달된 경우에만 처리
            if image_data_set is not None:
                department_board.image_set.all().delete()
                if image_data_set:
                    DepartmentBoardImage.objects.bulk_create(
                        [
                            DepartmentBoardImage(
                                department_board=department_board,
                                **image_data,
                            )
                            for image_data in image_data_set
                        ]
                    )

            # 파일이 명시적으로 전달된 경우에만 처리
            if file_data_set is not None:
                department_board.file_set.all().delete()
                if file_data_set:
                    DepartmentBoardFile.objects.bulk_create(
                        [
                            DepartmentBoardFile(
                                department_board=department_board,
                                **file_data,
                            )
                            for file_data in file_data_set
                        ]
                    )
        return department_board
