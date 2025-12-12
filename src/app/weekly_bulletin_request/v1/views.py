from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.weekly_bulletin_request.models import WeeklyBulletinRequest
from app.weekly_bulletin_request.v1.filters import WeeklyBulletinRequestFilter
from app.weekly_bulletin_request.v1.permissions import WeeklyBulletinRequestPermission
from app.weekly_bulletin_request.v1.serializers import WeeklyBulletinRequestSerializer


@extend_schema_view(
    create=extend_schema(summary="주보 원고 등록"),
)
class WeeklyBulletinRequestViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = WeeklyBulletinRequest.objects.all()
    serializer_class = WeeklyBulletinRequestSerializer
    permission_classes = [WeeklyBulletinRequestPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
