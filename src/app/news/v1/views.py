from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.news.models import News
from app.news.v1.filters import NewsFilter
from app.news.v1.permissions import NewsPermission
from app.news.v1.serializers import NewsSerializer


@extend_schema_view(
    list=extend_schema(summary="News 목록 조회"),
    create=extend_schema(summary="News 등록"),
    retrieve=extend_schema(summary="News 상세 조회"),
    update=extend_schema(summary="News 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="News 삭제"),
    latest=extend_schema(summary="최신 News 1건 조회 (비로그인 허용)"),
)
class NewsViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [NewsPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = NewsFilter

    def get_queryset(self):
        return super().get_queryset()

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")

    @action(methods=["get"], detail=False, permission_classes=[AllowAny])
    def latest(self, request):
        latest_news = self.get_queryset().first()
        if latest_news is None:
            return Response(None)
        serializer = self.get_serializer(latest_news)
        return Response(serializer.data, status=status.HTTP_200_OK)
