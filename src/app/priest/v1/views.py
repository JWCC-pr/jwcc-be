from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.priest.models import Priest, PriestRoleChoices
from app.priest.v1.filters import PriestFilter
from app.priest.v1.permissions import PriestPermission
from app.priest.v1.serializers import PriestSerializer


@extend_schema_view(
    list=extend_schema(summary="사제 목록 조회 (재임 중)"),
    update=extend_schema(summary="사제 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="사제 삭제"),
    history=extend_schema(summary="역대 사제 목록 조회"),
    pastor_history=extend_schema(summary="역대 주임신부 목록 조회"),
    associate_history=extend_schema(summary="역대 부주임/보좌신부 목록 조회"),
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

    @action(detail=False, methods=["get"], url_path="history")
    def history(self, request):
        queryset = self.queryset.filter(role__isnull=True, is_retired=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="pastor-history")
    def pastor_history(self, request):
        queryset = self.queryset.filter(role=PriestRoleChoices.PASTOR, is_retired=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="associate-history")
    def associate_history(self, request):
        queryset = self.queryset.filter(role=PriestRoleChoices.ASSOCIATE, is_retired=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
