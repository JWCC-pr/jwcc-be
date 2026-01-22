from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.religious.models import Religious
from app.religious.v1.filters import ReligiousFilter
from app.religious.v1.permissions import ReligiousPermission
from app.religious.v1.serializers import ReligiousSerializer


@extend_schema_view(
    list=extend_schema(summary="수도자 목록 조회 (재임 중)"),
    create=extend_schema(summary="수도자 등록"),
    update=extend_schema(summary="수도자 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="수도자 삭제"),
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
    pagination_class = None
    filterset_class = ReligiousFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
