from rest_framework import serializers

from app.sub_department.models import SubDepartment


class SubDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDepartment
        fields = ["id", "name"]
        ref_name = "UserSubDepartmentSerializer"
