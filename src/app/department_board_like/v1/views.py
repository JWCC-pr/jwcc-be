from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.department_board_like.models import DepartmentBoardLike
from app.department_board_like.v1.permissions import DepartmentBoardLikePermission
from app.department_board_like.v1.serializers import DepartmentBoardLikeToggleSerializer


@extend_schema_view(
    toggle=extend_schema(summary="분과 게시글 좋아요 토글", tags=["department_board_like"]),
)
class DepartmentBoardLikeViewSet(GenericViewSet):
    queryset = DepartmentBoardLike.objects.all()
    permission_classes = [DepartmentBoardLikePermission]

    @action(methods=["post"], detail=False, serializer_class=DepartmentBoardLikeToggleSerializer)
    def toggle(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
