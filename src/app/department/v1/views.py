from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department.models import Department
from app.department.v1.filters import DepartmentFilter
from app.department.v1.permissions import DepartmentPermission
from app.department.v1.serializers import DepartmentSerializer


@extend_schema_view(
    list=extend_schema(summary="분과 목록 조회"),
)
class DepartmentViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [DepartmentPermission]
    pagination_class = None
    filterset_class = DepartmentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
