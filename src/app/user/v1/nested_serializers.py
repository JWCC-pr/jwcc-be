from rest_framework import serializers

from app.department.models import Department
from app.sub_department.models import SubDepartment


class SubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDepartment
        fields = ["id", "name"]
        ref_name = "UserSubDepartmentSerializer"


class DepartmentSerializer(serializers.ModelSerializer):
    sub_department = SubDepartmentSerializer(label="세부 분과")

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "sub_department",
        ]
        ref_name = "UserDepartmentSerializer"
