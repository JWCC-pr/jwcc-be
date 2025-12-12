from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.passing_notice.models import PassingNotice
from app.passing_notice.v1.filters import PassingNoticeFilter
from app.passing_notice.v1.permissions import PassingNoticePermission
from app.passing_notice.v1.serializers import PassingNoticeSerializer


@extend_schema_view(
    list=extend_schema(summary="선종 안내 목록 조회"),
    retrieve=extend_schema(summary="선종 안내 상세 조회"),
)
class PassingNoticeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = PassingNotice.objects.all()
    serializer_class = PassingNoticeSerializer
    permission_classes = [PassingNoticePermission]
    pagination_class = LimitOffsetPagination
    filterset_class = PassingNoticeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
