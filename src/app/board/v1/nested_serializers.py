from rest_framework import serializers

from app.department.models import Department
from app.user.models import User


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]
        ref_name = "BoardDepartmentSerializer"


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
        ref_name = "BoardUserSerializer"
