from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.liturgy_flower.models import LiturgyFlower
from app.liturgy_flower.v1.filters import LiturgyFlowerFilter
from app.liturgy_flower.v1.permissions import LiturgyFlowerPermission
from app.liturgy_flower.v1.serializers import LiturgyFlowerSerializer


@extend_schema_view(
    list=extend_schema(summary="전례꽃 목록 조회"),
)
class LiturgyFlowerViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = LiturgyFlower.objects.all()
    serializer_class = LiturgyFlowerSerializer
    permission_classes = [LiturgyFlowerPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = LiturgyFlowerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("image_set")
        return queryset
