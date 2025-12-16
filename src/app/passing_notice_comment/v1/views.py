from django.db.models import BooleanField, Case, When
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.passing_notice_comment.models import PassingNoticeComment
from app.passing_notice_comment.v1.filters import PassingNoticeCommentFilter
from app.passing_notice_comment.v1.permissions import PassingNoticeCommentPermission
from app.passing_notice_comment.v1.serializers import PassingNoticeCommentSerializer


@extend_schema_view(
    list=extend_schema(summary="선종 안내 댓글 목록 조회", tags=["passing_notice_comment"]),
    create=extend_schema(summary="선종 안내 댓글 등록", tags=["passing_notice_comment"]),
    update=extend_schema(summary="선종 안내 댓글 수정", tags=["passing_notice_comment"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="선종 안내 댓글 삭제", tags=["passing_notice_comment"]),
)
class PassingNoticeCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = PassingNoticeComment.objects.all()
    serializer_class = PassingNoticeCommentSerializer
    permission_classes = [PassingNoticeCommentPermission]
    pagination_class = CursorPagination
    filterset_class = PassingNoticeCommentFilter
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
        queryset = queryset.prefetch_related("user__sub_department_set")
        if not self.request.query_params.get("parent_id"):
            queryset = queryset.filter(parent__isnull=True)
        return queryset
