from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department_board_like.v1.filters import DepartmentBoardLikeFilter
from app.department_board_like.v1.permissions import DepartmentBoardLikePermission
from app.department_board_like.v1.serializers import DepartmentBoardLikeSerializer
from app.department_board_like.models import DepartmentBoardLike


@extend_schema_view(
    list=extend_schema(summary="DepartmentBoardLike 목록 조회"),
    create=extend_schema(summary="DepartmentBoardLike 등록"),
    retrieve=extend_schema(summary="DepartmentBoardLike 상세 조회"),
    update=extend_schema(summary="DepartmentBoardLike 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="DepartmentBoardLike 삭제"),
)
class DepartmentBoardLikeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DepartmentBoardLike.objects.all()
    serializer_class = DepartmentBoardLikeSerializer
    permission_classes = [DepartmentBoardLikePermission]
    pagination_class = CursorPagination
    filterset_class = DepartmentBoardLikeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
