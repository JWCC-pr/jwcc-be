from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.pastor_history.v1.filters import PastorHistoryFilter
from app.pastor_history.v1.permissions import PastorHistoryPermission
from app.pastor_history.v1.serializers import PastorHistorySerializer
from app.pastor_history.models import PastorHistory


@extend_schema_view(
    list=extend_schema(summary="역대 주임신부 목록 조회"),
    create=extend_schema(summary="역대 주임신부 등록"),
    update=extend_schema(summary="역대 주임신부 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="역대 주임신부 삭제"),
)
class PastorHistoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = PastorHistory.objects.all()
    serializer_class = PastorHistorySerializer
    permission_classes = [PastorHistoryPermission]
    pagination_class = None
    filterset_class = PastorHistoryFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
