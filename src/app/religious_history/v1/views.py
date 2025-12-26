from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.religious_history.v1.filters import ReligiousHistoryFilter
from app.religious_history.v1.permissions import ReligiousHistoryPermission
from app.religious_history.v1.serializers import ReligiousHistorySerializer
from app.religious_history.models import ReligiousHistory


@extend_schema_view(
    list=extend_schema(summary="본당 출신 수도자 목록 조회"),
    create=extend_schema(summary="본당 출신 수도자 등록"),
    update=extend_schema(summary="본당 출신 수도자 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="본당 출신 수도자 삭제"),
)
class ReligiousHistoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = ReligiousHistory.objects.all()
    serializer_class = ReligiousHistorySerializer
    permission_classes = [ReligiousHistoryPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = ReligiousHistoryFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
