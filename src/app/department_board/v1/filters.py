import django_filters
from django.db.models import Q
from app.department_board.models import DepartmentBoard


class DepartmentBoardFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name="department_id", label="분과 ID")
    sub_department = django_filters.NumberFilter(field_name="sub_department_id", label="세부분과 ID")
    search = django_filters.CharFilter(method="filter_search", label="검색어")

    class Meta:
        model = DepartmentBoard
        fields = ["department", "sub_department", "search"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(body__icontains=value))
