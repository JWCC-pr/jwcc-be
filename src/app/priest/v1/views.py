from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.priest.models import Priest
from app.priest.v1.filters import PriestFilter
from app.priest.v1.permissions import PriestPermission
from app.priest.v1.serializers import PriestSerializer


@extend_schema_view(
    list=extend_schema(summary="사제 목록 조회"),
    create=extend_schema(summary="사제 등록"),
    retrieve=extend_schema(summary="사제 상세 조회"),
    update=extend_schema(summary="사제 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="사제 삭제"),
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
    pagination_class = None
    filterset_class = PriestFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
