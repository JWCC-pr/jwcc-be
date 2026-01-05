import django_filters

from app.department_board.models import DepartmentBoard


class DepartmentBoardFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name="department_id", label="분과 ID")

    class Meta:
        model = DepartmentBoard
        fields = ["department"]
