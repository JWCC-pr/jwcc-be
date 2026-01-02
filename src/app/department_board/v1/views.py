from django.db import transaction
from django.db.models import Case, When, BooleanField, Exists, OuterRef, F
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.department_board.v1.filters import DepartmentBoardFilter
from app.department_board.v1.permissions import DepartmentBoardPermission
from app.department_board.v1.serializers import DepartmentBoardSerializer
from app.department_board.models import DepartmentBoard
from app.department_board_hit.models import DepartmentBoardHit
from app.department_board_like.models import DepartmentBoardLike


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


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
    ordering_fields = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()

        user_department_ids = list(self.request.user.sub_department_set.values_list("department_id", flat=True))

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
            if request.user.is_authenticated:
                hit, created = DepartmentBoardHit.objects.get_or_create(
                    department_board_id=self.kwargs["pk"],
                    user_id=request.user.id,
                )
            else:
                ip_address = get_client_ip(request)
                hit, created = DepartmentBoardHit.objects.get_or_create(
                    department_board_id=self.kwargs["pk"],
                    ip_address=ip_address,
                )

            if created:
                DepartmentBoard.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            else:
                if hit.updated_at < timezone.localtime() - timezone.timedelta(minutes=10):
                    hit.updated_at = timezone.localtime()
                    hit.save()
                    DepartmentBoard.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            return super().retrieve(request, *args, **kwargs)
