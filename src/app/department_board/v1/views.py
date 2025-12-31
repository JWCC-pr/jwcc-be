from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department_board.v1.filters import DepartmentBoardFilter
from app.department_board.v1.permissions import DepartmentBoardPermission
from app.department_board.v1.serializers import DepartmentBoardSerializer
from app.department_board.models import DepartmentBoard


@extend_schema_view(
    list=extend_schema(summary="DepartmentBoard 목록 조회"),
    create=extend_schema(summary="DepartmentBoard 등록"),
    retrieve=extend_schema(summary="DepartmentBoard 상세 조회"),
    update=extend_schema(summary="DepartmentBoard 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="DepartmentBoard 삭제"),
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
    pagination_class = CursorPagination
    filterset_class = DepartmentBoardFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
