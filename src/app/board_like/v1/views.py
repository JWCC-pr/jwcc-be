from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.board_like.models import BoardLike
from app.board_like.v1.permissions import BoardLikePermission
from app.board_like.v1.serializers import BoardLikeToggleSerializer


@extend_schema_view(
    toggle=extend_schema(summary="자유 게시글 좋아요 토글", tags=["board_like"]),
)
class BoardLikeViewSet(
    GenericViewSet,
):
    queryset = BoardLike.objects.all()
    permission_classes = [BoardLikePermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(methods=["post"], detail=False, serializer_class=BoardLikeToggleSerializer)
    def toggle(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
