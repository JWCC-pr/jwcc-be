from django.db.models import BooleanField, Case, When
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.liturgy_flower_comment.models import LiturgyFlowerComment
from app.liturgy_flower_comment.v1.filters import LiturgyFlowerCommentFilter
from app.liturgy_flower_comment.v1.permissions import LiturgyFlowerCommentPermission
from app.liturgy_flower_comment.v1.serializers import LiturgyFlowerCommentSerializer


@extend_schema_view(
    list=extend_schema(summary="전례꽃 댓글 목록 조회", tags=["liturgy_flower_comment"]),
    create=extend_schema(summary="전례꽃 댓글 등록", tags=["liturgy_flower_comment"]),
    update=extend_schema(summary="전례꽃 댓글 수정", tags=["liturgy_flower_comment"]),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="전례꽃 댓글 삭제", tags=["liturgy_flower_comment"]),
)
class LiturgyFlowerCommentViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = LiturgyFlowerComment.objects.all()
    serializer_class = LiturgyFlowerCommentSerializer
    permission_classes = [LiturgyFlowerCommentPermission]
    pagination_class = CursorPagination
    filterset_class = LiturgyFlowerCommentFilter
    ordering = "created_at"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(liturgy_flower_id=self.kwargs["liturgy_flower_id"])
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
        )
        queryset = queryset.prefetch_related("user__sub_department_set")
        return queryset

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
