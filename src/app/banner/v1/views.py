from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.banner.models import Banner
from app.banner.v1.filters import BannerFilter
from app.banner.v1.permissions import BannerPermission
from app.banner.v1.serializers import BannerSerializer
from app.common.pagination import CursorPagination


@extend_schema_view(
    list=extend_schema(summary="배너 목록 조회"),
)
class BannerViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [BannerPermission]
    pagination_class = None
    filterset_class = BannerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
