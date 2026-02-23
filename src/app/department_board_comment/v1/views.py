from django.db.models import BooleanField, Case, When
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department_board_comment.models import DepartmentBoardComment
from app.department_board_comment.v1.filters import DepartmentBoardCommentFilter
from app.department_board_comment.v1.permissions import DepartmentBoardCommentPermission
from app.department_board_comment.v1.serializers import DepartmentBoardCommentSerializer


@extend_schema_view(
    list=extend_schema(summary="분과 게시글 댓글 목록 조회", tags=["department_board_comment"]),
    create=extend_schema(summary="분과 게시글 댓글 등록", tags=["department_board_comment"]),
    update=extend_schema(summary="분과 게시글 댓글 수정", tags=["department_board_comment"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="분과 게시글 댓글 삭제", tags=["department_board_comment"]),
)
class DepartmentBoardCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DepartmentBoardComment.objects.all()
    serializer_class = DepartmentBoardCommentSerializer
    permission_classes = [DepartmentBoardCommentPermission]
    pagination_class = CursorPagination
    filterset_class = DepartmentBoardCommentFilter
    ordering = "created_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(department_board_id=self.kwargs["department_board_id"])
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        )
        queryset = queryset.prefetch_related("user__sub_department_set")
        return queryset
