from django.db import transaction
from rest_framework import serializers

from app.board.v1.nested_serializers import UserSerializer
from app.department_board.models import DepartmentBoard
from app.department_board.v1.nested_serializers import (
    DepartmentBoardFileSerializer,
    DepartmentBoardImageSerializer,
    SubDepartmentSerializer,
)
from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage
from app.sub_department.models import SubDepartment
from app.user.models import UserGradeChoices


class DepartmentBoardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sub_department = serializers.PrimaryKeyRelatedField(
        queryset=SubDepartment.objects.all(),
        label="세부분과 ID",
    )
    sub_department_info = SubDepartmentSerializer(
        source="sub_department",
        read_only=True,
        label="세부분과",
    )
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
            "sub_department_info",
            "title",
            "body",
            "is_pinned",
            "is_secret",
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

    def _validate_pin_limit(self, instance, sub_department, is_pinned):
        if not is_pinned:
            return

        department_id = None
        if sub_department:
            department_id = sub_department.department_id
        elif instance:
            department_id = instance.department_id

        if not department_id:
            return

        qs = DepartmentBoard.objects.filter(department_id=department_id, is_pinned=True)
        if instance and instance.pk:
            qs = qs.exclude(pk=instance.pk)

        if qs.count() >= 5:
            raise serializers.ValidationError({"is_pinned": "분과별 고정 게시글은 최대 5개까지 등록할 수 있습니다."})

    def _validate_pin_permission(self, instance, sub_department, is_pinned):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return

        allowed_grades = {
            UserGradeChoices.GRADE_01,
            UserGradeChoices.GRADE_02,
            UserGradeChoices.GRADE_03,
            UserGradeChoices.GRADE_04,
        }

        if instance and instance.is_pinned and not is_pinned:
            if user.grade != UserGradeChoices.GRADE_01 and instance.user_id != user.id:
                raise serializers.ValidationError({"is_pinned": "자신이 등록한 공지만 해제할 수 있습니다."})
            return

        if is_pinned:
            if user.grade not in allowed_grades:
                raise serializers.ValidationError({"is_pinned": "공지글 작성 권한이 없습니다."})

            if instance and instance.pk and user.grade != UserGradeChoices.GRADE_01 and instance.user_id != user.id:
                raise serializers.ValidationError({"is_pinned": "자신이 등록한 공지만 수정할 수 있습니다."})

    def validate(self, attrs):
        instance = getattr(self, "instance", None)
        sub_department = attrs.get("sub_department", getattr(instance, "sub_department", None))
        is_pinned = attrs.get("is_pinned", getattr(instance, "is_pinned", False))
        self._validate_pin_permission(instance, sub_department, is_pinned)
        self._validate_pin_limit(instance, sub_department, is_pinned)
        return attrs

    def validate_sub_department(self, value):
        user = self.context["request"].user
        if not user.sub_department_set.filter(id=value.id).exists():
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
