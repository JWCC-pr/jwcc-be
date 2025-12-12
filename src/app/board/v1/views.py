from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.board.models import Board
from app.board.v1.filters import BoardFilter
from app.board.v1.permissions import BoardPermission
from app.board.v1.serializers import BoardSerializer
from app.common.pagination import CursorPagination


@extend_schema_view(
    list=extend_schema(summary="Board 목록 조회"),
    create=extend_schema(summary="Board 등록"),
    retrieve=extend_schema(summary="Board 상세 조회"),
    update=extend_schema(summary="Board 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="Board 삭제"),
)
class BoardViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [BoardPermission]
    pagination_class = CursorPagination
    filterset_class = BoardFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
