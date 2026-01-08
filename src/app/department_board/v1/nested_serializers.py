from rest_framework import serializers

from app.department_board_file.models import DepartmentBoardFile
from app.department_board_image.models import DepartmentBoardImage


class DepartmentBoardFileSerializer(serializers.ModelSerializer):
    file = serializers.URLField(label="파일")

    class Meta:
        model = DepartmentBoardFile
        fields = ["id", "file", "file_name"]
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
