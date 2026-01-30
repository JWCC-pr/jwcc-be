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
            "image_set",
            "file_set",
            "is_owned",
            "is_liked",
            "hit_count",
            "comment_count",
            "like_count",
            "is_modified",
            "is_pinned",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["department"]

    def validate_sub_department(self, value):
        user = self.context["request"].user
        if user.grade == UserGradeChoices.GRADE_01:
            return value
        if user.grade == UserGradeChoices.GRADE_05 or user.sub_department_set.filter(name="명도회").exists():
            if value.department.name == "사목협의회":
                raise serializers.ValidationError("사목협의회에는 글을 작성할 수 없습니다.")
            return value
        if not user.sub_department_set.filter(id=value.id).exists():
            raise serializers.ValidationError("소속된 세부분과만 선택할 수 있습니다.")
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        is_pinned = attrs.get("is_pinned", False)

        if is_pinned:
            user = self.context["request"].user
            # 단체장(GRADE_04) 이하만 고정글 설정 가능
            if user.grade > UserGradeChoices.GRADE_04:
                raise serializers.ValidationError({"is_pinned": "고정글 설정 권한이 없습니다."})

            # sub_department별 최대 5개 제한
            sub_department = attrs.get("sub_department") or (self.instance.sub_department if self.instance else None)
            if sub_department:
                pinned_count = (
                    DepartmentBoard.objects.filter(
                        sub_department=sub_department,
                        is_pinned=True,
                    )
                    .exclude(id=self.instance.id if self.instance else None)
                    .count()
                )

                if pinned_count >= 5:
                    raise serializers.ValidationError({"is_pinned": "고정글은 최대 5개까지만 등록할 수 있습니다."})

        return attrs

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
