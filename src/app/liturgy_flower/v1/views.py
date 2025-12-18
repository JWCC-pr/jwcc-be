from django.db import transaction
from django.db.models import Case, When, BooleanField, Exists, OuterRef, F
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower.v1.filters import LiturgyFlowerFilter
from app.liturgy_flower.v1.permissions import LiturgyFlowerPermission
from app.liturgy_flower.v1.serializers import LiturgyFlowerSerializer
from app.liturgy_flower_hit.models import LiturgyFlowerHit
from app.liturgy_flower_like.models import LiturgyFlowerLike


def get_client_ip(request):
    """클라이언트의 IP 주소를 반환합니다."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@extend_schema_view(
    list=extend_schema(summary="전례꽃 목록 조회"),
    create=extend_schema(summary="전례꽃 생성"),
    retrieve=extend_schema(summary="전례꽃 상세 조회"),
    update=extend_schema(summary="전례꽃 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="전례꽃 삭제"),
)
class LiturgyFlowerViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = LiturgyFlower.objects.all()
    serializer_class = LiturgyFlowerSerializer
    permission_classes = [LiturgyFlowerPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = LiturgyFlowerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(
            is_owned=Case(
                When(user_id=self.request.user.id, then=True),
                default=False,
                output_field=BooleanField(),
            ),
            is_liked=Exists(
                LiturgyFlowerLike.objects.filter(liturgy_flower_id=OuterRef("id"), user_id=self.request.user.id)
            ),
        )
        queryset = queryset.prefetch_related("image_set", "user__sub_department_set")
        return queryset

    def retrieve(self, request, *args, **kwargs):
        with transaction.atomic():
            # 로그인 사용자인 경우 user_id로, 비로그인 사용자인 경우 ip_address로 조회
            if request.user.is_authenticated:
                hit, created = LiturgyFlowerHit.objects.get_or_create(
                    liturgy_flower_id=self.kwargs["pk"],
                    user_id=request.user.id,
                )
            else:
                ip_address = get_client_ip(request)
                hit, created = LiturgyFlowerHit.objects.get_or_create(
                    liturgy_flower_id=self.kwargs["pk"],
                    ip_address=ip_address,
                )

            if created:
                LiturgyFlower.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            else:
                if hit.updated_at < timezone.localtime() - timezone.timedelta(minutes=10):
                    hit.updated_at = timezone.localtime()
                    hit.save()
                    LiturgyFlower.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            return super().retrieve(request, *args, **kwargs)
