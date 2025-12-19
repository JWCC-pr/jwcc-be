from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.schedule.models import Schedule
from app.schedule.v1.filters import ScheduleFilter
from app.schedule.v1.permissions import SchedulePermission
from app.schedule.v1.serializers import ScheduleSerializer


@extend_schema_view(
    list=extend_schema(summary="일정 목록 조회"),
)
class ScheduleViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [SchedulePermission]
    pagination_class = None
    filterset_class = ScheduleFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
