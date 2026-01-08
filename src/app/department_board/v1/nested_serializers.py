from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage
from app.sub_department.models import SubDepartment


@extend_schema_field(serializers.IntegerField(label="세부분과 ID"))
class SubDepartmentSerializer(serializers.Serializer):
    id = serializers.IntegerField(label="세부분과 ID", read_only=True)
    name = serializers.CharField(label="세부분과명", read_only=True)

    class Meta:
        ref_name = "DepartmentBoardSubDepartmentSerializer"

    def to_representation(self, instance):
        return {"id": instance.id, "name": instance.name}

    def to_internal_value(self, data):
        if isinstance(data, int):
            try:
                return SubDepartment.objects.get(id=data)
            except SubDepartment.DoesNotExist:
                raise serializers.ValidationError("존재하지 않는 세부분과입니다.")
        raise serializers.ValidationError("세부분과 ID(정수)를 입력해주세요.")


class DepartmentBoardFileSerializer(serializers.ModelSerializer):
    file = serializers.URLField(label="파일")

    class Meta:
        model = DepartmentBoardFile
        fields = ["id", "file"]
        ref_name = "DepartmentBoardFileNestedSerializer"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["file"] = instance.file.url
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["file"] = ret["file"].replace(DepartmentBoardFile._meta.get_field("file").storage.url(""), "")
        return ret


class DepartmentBoardImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(label="이미지")

    class Meta:
        model = DepartmentBoardImage
        fields = ["id", "image"]
        ref_name = "DepartmentBoardImageNestedSerializer"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["image"] = instance.image.url
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["image"] = ret["image"].replace(DepartmentBoardImage._meta.get_field("image").storage.url(""), "")
        return ret
