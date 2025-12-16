from rest_framework import serializers

from app.department.models import Department
from app.department.v1.nested_serializers import SubDepartmentSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    sub_department_set = SubDepartmentSerializer(label="세부분과", many=True)

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "sub_department_set",
        ]
