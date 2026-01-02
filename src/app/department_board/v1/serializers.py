from django.db import transaction
from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.department.models import Department
from app.department_board.models import DepartmentBoard
from app.department_board_image.models import DepartmentBoardImage
from app.department_board_image.v1.serializers import DepartmentBoardImageSerializer


class DepartmentBoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(label="유저", read_only=True)
    department = serializers.PrimaryKeyRelatedField(label="분과", queryset=Department.objects.all())
    is_owned = serializers.BooleanField(label="소유 여부", read_only=True)
    is_liked = serializers.BooleanField(label="좋아요 여부", read_only=True)
    # image_set = DepartmentBoardImageSerializer(label="이미지", many=True)

    class Meta:
        model = DepartmentBoard
        fields = [
            "id",
            "user",
            "department",
            "sub_department_set",
            "title",
            "body",
            # "image_set",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
            "is_modified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["sub_department_set"]

    def validate_department(self, value):
        user = self.context["request"].user
        user_department_ids = user.sub_department_set.values_list("department_id", flat=True)
        if value.id not in user_department_ids:
            raise serializers.ValidationError("소속된 분과만 선택할 수 있습니다.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            # image_data_set = validated_data.pop("image_set")
            user = self.context["request"].user
            validated_data["user"] = user
            department = validated_data["department"]

            department_board = DepartmentBoard.objects.create(**validated_data)

            # user의 sub_department 중 선택한 department에 속한 것들을 설정
            user_sub_departments = user.sub_department_set.filter(department=department)
            department_board.sub_department_set.set(user_sub_departments)

            # DepartmentBoardImage.objects.bulk_create(
            #     [
            #         DepartmentBoardImage(
            #             department_board=department_board,
            #             **image_data,
            #         )
            #         for image_data in image_data_set
            #     ]
            # )
        return department_board

    def update(self, instance, validated_data):
        with transaction.atomic():
            validated_data["is_modified"] = True
            # image_data_set = validated_data.pop("image_set")
            department_board = super().update(instance, validated_data)
            # department_board.image_set.all().delete()
            # DepartmentBoardImage.objects.bulk_create(
            #     [
            #         DepartmentBoardImage(
            #             department_board=department_board,
            #             **image_data,
            #         )
            #         for image_data in image_data_set
            #     ]
            # )
        return department_board
