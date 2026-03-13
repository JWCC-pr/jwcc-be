from django.db import transaction
from django.db.models import Case, When, BooleanField, Exists, OuterRef, F, Q

from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.department_board.models import DepartmentBoard
from app.department_board.v1.filters import DepartmentBoardFilter
from app.department_board.v1.permissions import DepartmentBoardPermission
from app.department_board.v1.serializers import DepartmentBoardSerializer
from app.department_board_hit.models import DepartmentBoardHit
from app.department_board_like.models import DepartmentBoardLike
from app.user.models import UserGradeChoices


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
    ordering_fields = ["-created_at", "-hit_count"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        department_id = self.request.query_params.get("department")
        if department_id:
            queryset = queryset.filter(department_id=department_id)
            if self.request.user.grade > UserGradeChoices.GRADE_04:
                allowed_sub_departments = self.request.user.sub_department_set.values_list("id", flat=True)
                queryset = queryset.filter(
                    Q(is_secret=False) | Q(is_secret=True, sub_department_id__in=allowed_sub_departments)
                )
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

    def list(self, request, *args, **kwargs):
        if not request.query_params.get("department"):
            raise ValidationError({"department": ["이 필드는 필수 항목입니다."]})
        return super().list(request, *args, **kwargs)

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
