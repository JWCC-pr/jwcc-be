from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.notice.models import Notice
from app.notice.v1.filters import NoticeFilter
from app.notice.v1.permissions import NoticePermission
from app.notice.v1.serializers import NoticeSerializer


@extend_schema_view(
    list=extend_schema(summary="공지사항 목록 조회"),
    retrieve=extend_schema(summary="공지사항 상세 조회"),
)
class NoticeViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [NoticePermission]
    pagination_class = LimitOffsetPagination
    filterset_class = NoticeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
