from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.priest.v1.filters import PriestFilter
from app.priest.v1.permissions import PriestPermission
from app.priest.v1.serializers import PriestSerializer
from app.priest.models import Priest


@extend_schema_view(
    list=extend_schema(summary="사제 목록 조회 (재임 중)"),
    create=extend_schema(summary="사제 등록"),
    retrieve=extend_schema(summary="사제 상세 조회"),
    update=extend_schema(summary="사제 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="사제 삭제"),
    history=extend_schema(summary="역대 사제 목록 조회"),
)
class PriestViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Priest.objects.all()
    serializer_class = PriestSerializer
    permission_classes = [PriestPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = PriestFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "list":
            queryset = queryset.filter(is_retired=False)
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")

    @action(detail=False, methods=["get"], url_path="history")
    def history(self, request):
        queryset = self.queryset.filter(is_retired=True)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
