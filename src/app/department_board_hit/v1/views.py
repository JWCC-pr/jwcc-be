from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.department_board_hit.models import DepartmentBoardHit
from app.department_board_hit.v1.filters import DepartmentBoardHitFilter
from app.department_board_hit.v1.permissions import DepartmentBoardHitPermission
from app.department_board_hit.v1.serializers import DepartmentBoardHitSerializer


@extend_schema_view(
    list=extend_schema(summary="DepartmentBoardHit 목록 조회"),
    create=extend_schema(summary="DepartmentBoardHit 등록"),
    retrieve=extend_schema(summary="DepartmentBoardHit 상세 조회"),
    update=extend_schema(summary="DepartmentBoardHit 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="DepartmentBoardHit 삭제"),
)
class DepartmentBoardHitViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = DepartmentBoardHit.objects.all()
    serializer_class = DepartmentBoardHitSerializer
    permission_classes = [DepartmentBoardHitPermission]
    pagination_class = CursorPagination
    filterset_class = DepartmentBoardHitFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
