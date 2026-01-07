from django.db import transaction
from django.db.models import Case, When, BooleanField, Exists, OuterRef, F
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.department_board.v1.filters import DepartmentBoardFilter
from app.department_board.v1.permissions import DepartmentBoardPermission
from app.department_board.v1.serializers import DepartmentBoardSerializer
from app.department_board.models import DepartmentBoard
from app.department_board_hit.models import DepartmentBoardHit
from app.department_board_like.models import DepartmentBoardLike


@extend_schema_view(
    list=extend_schema(summary="분과 게시글 목록 조회"),
    create=extend_schema(summary="분과 게시글 등록"),
    retrieve=extend_schema(summary="분과 게시글 상세 조회"),
    update=extend_schema(summary="분과 게시글 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="분과 게시글 삭제"),
)
class DepartmentBoardViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DepartmentBoard.objects.all()
    serializer_class = DepartmentBoardSerializer
    permission_classes = [DepartmentBoardPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = DepartmentBoardFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["created_at", "like_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            is_liked=Exists(
                DepartmentBoardLike.objects.filter(department_board_id=OuterRef("id"), user_id=self.request.user.id)
            ),
        )
        queryset = queryset.prefetch_related("user__sub_department_set")
        return queryset

    def retrieve(self, request, *args, **kwargs):
        with transaction.atomic():
            hit, created = DepartmentBoardHit.objects.get_or_create(
                department_board_id=self.kwargs["pk"],
                user_id=request.user.id,
            )

            if created:
                DepartmentBoard.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            else:
                if hit.updated_at < timezone.localtime() - timezone.timedelta(minutes=10):
                    hit.updated_at = timezone.localtime()
                    hit.save()
                    DepartmentBoard.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            return super().retrieve(request, *args, **kwargs)
