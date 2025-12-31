from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department_board_comment.v1.filters import DepartmentBoardCommentFilter
from app.department_board_comment.v1.permissions import DepartmentBoardCommentPermission
from app.department_board_comment.v1.serializers import DepartmentBoardCommentSerializer
from app.department_board_comment.models import DepartmentBoardComment


@extend_schema_view(
    list=extend_schema(summary="DepartmentBoardComment 목록 조회"),
    create=extend_schema(summary="DepartmentBoardComment 등록"),
    retrieve=extend_schema(summary="DepartmentBoardComment 상세 조회"),
    update=extend_schema(summary="DepartmentBoardComment 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="DepartmentBoardComment 삭제"),
)
class DepartmentBoardCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DepartmentBoardComment.objects.all()
    serializer_class = DepartmentBoardCommentSerializer
    permission_classes = [DepartmentBoardCommentPermission]
    pagination_class = CursorPagination
    filterset_class = DepartmentBoardCommentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
