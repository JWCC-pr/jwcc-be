from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.priest_history.v1.filters import PriestHistoryFilter
from app.priest_history.v1.permissions import PriestHistoryPermission
from app.priest_history.v1.serializers import PriestHistorySerializer
from app.priest_history.models import PriestHistory


@extend_schema_view(
    list=extend_schema(summary="PriestHistory 목록 조회"),
    create=extend_schema(summary="PriestHistory 등록"),
    update=extend_schema(summary="PriestHistory 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="PriestHistory 삭제"),
)
class PriestHistoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = PriestHistory.objects.all()
    serializer_class = PriestHistorySerializer
    permission_classes = [PriestHistoryPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = PriestHistoryFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
