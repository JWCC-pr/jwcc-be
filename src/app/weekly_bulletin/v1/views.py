from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.weekly_bulletin.models import WeeklyBulletin
from app.weekly_bulletin.v1.filters import WeeklyBulletinFilter
from app.weekly_bulletin.v1.permissions import WeeklyBulletinPermission
from app.weekly_bulletin.v1.serializers import WeeklyBulletinSerializer


@extend_schema_view(
    list=extend_schema(summary="주보 목록 조회"),
    retrieve=extend_schema(summary="주보 상세 조회"),
)
class WeeklyBulletinViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = WeeklyBulletin.objects.all()
    serializer_class = WeeklyBulletinSerializer
    permission_classes = [WeeklyBulletinPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = WeeklyBulletinFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
