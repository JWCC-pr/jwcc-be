from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.religious.v1.filters import ReligiousFilter
from app.religious.v1.permissions import ReligiousPermission
from app.religious.v1.serializers import ReligiousSerializer
from app.religious.models import Religious


@extend_schema_view(
    list=extend_schema(summary="수도자 목록 조회 (재임 중)"),
    create=extend_schema(summary="수도자 등록"),
    retrieve=extend_schema(summary="수도자 상세 조회"),
    update=extend_schema(summary="수도자 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="수도자 삭제"),
    retired=extend_schema(summary="퇴임 수도자 목록 조회"),
)
class ReligiousViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Religious.objects.all()
    serializer_class = ReligiousSerializer
    permission_classes = [ReligiousPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = ReligiousFilter

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
