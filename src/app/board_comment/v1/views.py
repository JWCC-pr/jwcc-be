from django.db.models import BooleanField, Case, When
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.board_comment.models import BoardComment
from app.board_comment.v1.filters import BoardCommentFilter
from app.board_comment.v1.permissions import BoardCommentPermission
from app.board_comment.v1.serializers import BoardCommentSerializer
from app.common.pagination import CursorPagination


@extend_schema_view(
    list=extend_schema(summary="자유 게시글 댓글 목록 조회", tags=["board_comment"]),
    create=extend_schema(summary="자유 게시글 댓글 등록", tags=["board_comment"]),
    update=extend_schema(summary="자유 게시글 댓글 수정", tags=["board_comment"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="자유 게시글 댓글 삭제", tags=["board_comment"]),
)
class BoardCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = BoardComment.objects.all()
    serializer_class = BoardCommentSerializer
    permission_classes = [BoardCommentPermission]
    pagination_class = CursorPagination
    filterset_class = BoardCommentFilter
    ordering = "-created_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        )
        queryset = queryset.prefetch_related("user__department_set")
        if not self.request.query_params.get("parent_id"):
            queryset = queryset.filter(parent__isnull=True)
        return queryset
