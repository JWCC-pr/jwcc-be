from django.db import transaction
from django.db.models import BooleanField, Case, Exists, F, OuterRef, When
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.board.models import Board
from app.board.v1.filters import BoardFilter
from app.board.v1.permissions import BoardPermission
from app.board.v1.serializers import BoardSerializer
from app.board_hit.models import BoardHit
from app.board_like.models import BoardLike
from app.common.pagination import CursorPagination, LimitOffsetPagination


def get_client_ip(request):
    """클라이언트의 IP 주소를 반환합니다."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@extend_schema_view(
    list=extend_schema(summary="자유 게시글 목록 조회"),
    create=extend_schema(summary="자유 게시글 등록"),
    retrieve=extend_schema(summary="자유 게시글 상세 조회"),
    update=extend_schema(summary="자유 게시글 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="자유 게시글 삭제"),
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
    pagination_class = LimitOffsetPagination
    filterset_class = BoardFilter
    ordering_fields = ["-created_at", "-like_count"]
    # 솔팅 추가 필요

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            is_liked=Exists(BoardLike.objects.filter(board_id=OuterRef("id"), user_id=self.request.user.id)),
        )
        queryset = queryset.prefetch_related("user__department_set")
        return queryset

    def retrieve(self, request, *args, **kwargs):
        with transaction.atomic():
            # 로그인 사용자인 경우 user_id로, 비로그인 사용자인 경우 ip_address로 조회
            if request.user.is_authenticated:
                hit, created = BoardHit.objects.get_or_create(
                    board_id=self.kwargs["pk"],
                    user_id=request.user.id,
                )
            else:
                ip_address = get_client_ip(request)
                hit, created = BoardHit.objects.get_or_create(
                    board_id=self.kwargs["pk"],
                    ip_address=ip_address,
                )

            if created:
                Board.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            else:
                if hit.updated_at < timezone.localtime() - timezone.timedelta(minutes=10):
                    hit.updated_at = timezone.localtime()
                    hit.save()
                    Board.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            return super().retrieve(request, *args, **kwargs)
