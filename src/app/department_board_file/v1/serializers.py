from rest_framework import serializers

from app.department_board_file.models import DepartmentBoardFile


class DepartmentBoardFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentBoardFile
        fields = [
            "id",
            "file",
        ]
