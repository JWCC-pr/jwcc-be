from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.weekly_bulletin_editorial.models import WeeklyBulletinEditorial, WeeklyBulletinEditorialStateChoices
from app.weekly_bulletin_editorial.v1.filters import WeeklyBulletinEditorialFilter
from app.weekly_bulletin_editorial.v1.permissions import WeeklyBulletinEditorialPermission
from app.weekly_bulletin_editorial.v1.serializers import WeeklyBulletinEditorialSerializer


class BaseEditorialViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = WeeklyBulletinEditorial.objects.all()
    serializer_class = WeeklyBulletinEditorialSerializer
    permission_classes = [WeeklyBulletinEditorialPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = WeeklyBulletinEditorialFilter
    state_value = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("file_set")
        if self.state_value is not None:
            queryset = queryset.filter(state=self.state_value)
        return queryset

    def perform_create(self, serializer):
        if self.state_value is not None:
            serializer.save(state=self.state_value)
        else:
            serializer.save()

    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)


@extend_schema_view(
    list=extend_schema(summary="편집본 목록 조회"),
    create=extend_schema(summary="편집본 등록"),
    retrieve=extend_schema(summary="편집본 상세 조회"),
    partial_update=extend_schema(summary="편집본 수정"),
    destroy=extend_schema(summary="편집본 삭제"),
)
class DraftViewSet(BaseEditorialViewSet):
    state_value = WeeklyBulletinEditorialStateChoices.DRAFT


@extend_schema_view(
    list=extend_schema(summary="명도회 자료 목록 조회"),
    create=extend_schema(summary="명도회 자료 등록"),
    retrieve=extend_schema(summary="명도회 자료 상세 조회"),
    partial_update=extend_schema(summary="명도회 자료 수정"),
    destroy=extend_schema(summary="명도회 자료 삭제"),
)
class MyeongdoViewSet(BaseEditorialViewSet):
    state_value = WeeklyBulletinEditorialStateChoices.MYEONGDO


@extend_schema_view(
    list=extend_schema(summary="최종본 목록 조회"),
    create=extend_schema(summary="최종본 등록"),
    retrieve=extend_schema(summary="최종본 상세 조회"),
    partial_update=extend_schema(summary="최종본 수정"),
    destroy=extend_schema(summary="최종본 삭제"),
)
class FinalViewSet(BaseEditorialViewSet):
    state_value = WeeklyBulletinEditorialStateChoices.FINAL


@extend_schema_view(
    list=extend_schema(summary="양식 목록 조회"),
    create=extend_schema(summary="양식 등록"),
    retrieve=extend_schema(summary="양식 상세 조회"),
    partial_update=extend_schema(summary="양식 수정"),
    destroy=extend_schema(summary="양식 삭제"),
)
class TemplateViewSet(BaseEditorialViewSet):
    state_value = WeeklyBulletinEditorialStateChoices.TEMPLATE
