from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.liturgy_flower_like.models import LiturgyFlowerLike
from app.liturgy_flower_like.v1.permissions import LiturgyFlowerLikePermission
from app.liturgy_flower_like.v1.serializers import LiturgyFlowerLikeToggleSerializer


@extend_schema_view(
    toggle=extend_schema(summary="전례꽃 좋아요 토글", tags=["liturgy_flower_like"]),
)
class LiturgyFlowerLikeViewSet(
    GenericViewSet,
):
    queryset = LiturgyFlowerLike.objects.all()
    permission_classes = [LiturgyFlowerLikePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(methods=["post"], detail=False, serializer_class=LiturgyFlowerLikeToggleSerializer)
    def toggle(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
