from django.db import transaction
from django.db.models import F
from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.weekly_bulletin.models import WeeklyBulletin
from app.weekly_bulletin.v1.filters import WeeklyBulletinFilter
from app.weekly_bulletin.v1.permissions import WeeklyBulletinPermission
from app.weekly_bulletin.v1.serializers import WeeklyBulletinSerializer
from app.weekly_bulletin_hit.models import WeeklyBulletinHit


def get_client_ip(request):
    """클라이언트의 IP 주소를 반환합니다."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@extend_schema_view(
    list=extend_schema(summary="주보 목록 조회"),
    retrieve=extend_schema(summary="주보 상세 조회"),
)
class WeeklyBulletinViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = WeeklyBulletin.objects.all()
    serializer_class = WeeklyBulletinSerializer
    permission_classes = [WeeklyBulletinPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = WeeklyBulletinFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        with transaction.atomic():
            # 로그인 사용자인 경우 user_id로, 비로그인 사용자인 경우 ip_address로 조회
            if request.user.is_authenticated:
                hit, created = WeeklyBulletinHit.objects.get_or_create(
                    weekly_bulletin_id=self.kwargs["pk"],
                    user_id=request.user.id,
                )
            else:
                ip_address = get_client_ip(request)
                hit, created = WeeklyBulletinHit.objects.get_or_create(
                    weekly_bulletin_id=self.kwargs["pk"],
                    ip_address=ip_address,
                )

            if created:
                WeeklyBulletin.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            else:
                if hit.updated_at < timezone.localtime() - timezone.timedelta(minutes=10):
                    hit.updated_at = timezone.localtime()
                    hit.save()
                    WeeklyBulletin.objects.filter(id=self.kwargs["pk"]).update(hit_count=F("hit_count") + 1)
            return super().retrieve(request, *args, **kwargs)
