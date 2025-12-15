from rest_framework import serializers

from app.department.models import Department
from app.liturgy_flower_image.models import LiturgyFlowerImage
from app.user.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]
        ref_name = "LiturgyFlowerDepartmentSerializer"


class UserSerializer(serializers.ModelSerializer):
    department_set = DepartmentSerializer(label="분과", many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "baptismal_name",
            "department_set",
        ]
        ref_name = "LiturgyFlowerUserSerializer"


class LiturgyFlowerImageSerializer(serializers.ModelSerializer):
    image = serializers.URLField(label="이미지")

    class Meta:
        model = LiturgyFlowerImage
        fields = ["id", "image"]
        ref_name = "LiturgyFlowerImageSerializer"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["image"] = instance.image.url
        return ret

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret["image"] = ret["image"].replace(LiturgyFlowerImage._meta.get_field("image").storage.url(""), "")
        return ret
