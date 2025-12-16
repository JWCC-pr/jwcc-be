from rest_framework import serializers

from app.department.models import Department
from app.sub_department.models import SubDepartment
from app.user.models import User


class SubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDepartment
        fields = ["id", "name"]
        ref_name = "BoardCommentDepartmentSerializer"


class UserSerializer(serializers.ModelSerializer):
    sub_department_set = SubDepartmentSerializer(label="분과", many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "baptismal_name",
            "sub_department_set",
        ]
        ref_name = "BoardCommentUserSerializer"
