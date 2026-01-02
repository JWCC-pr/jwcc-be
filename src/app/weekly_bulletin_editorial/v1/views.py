from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.weekly_bulletin_editorial.v1.filters import WeeklyBulletinEditorialFilter
from app.weekly_bulletin_editorial.v1.permissions import WeeklyBulletinEditorialPermission
from app.weekly_bulletin_editorial.v1.serializers import WeeklyBulletinEditorialSerializer
from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial


@extend_schema_view(
    list=extend_schema(summary="WeeklyBulletinEditorial 목록 조회"),
    create=extend_schema(summary="WeeklyBulletinEditorial 등록"),
    retrieve=extend_schema(summary="WeeklyBulletinEditorial 상세 조회"),
    update=extend_schema(summary="WeeklyBulletinEditorial 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="WeeklyBulletinEditorial 삭제"),
)
class WeeklyBulletinEditorialViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = WeeklyBulletinEditorial.objects.all()
    serializer_class = WeeklyBulletinEditorialSerializer
    permission_classes = [WeeklyBulletinEditorialPermission]
    pagination_class = CursorPagination
    filterset_class = WeeklyBulletinEditorialFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("file_set")
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
