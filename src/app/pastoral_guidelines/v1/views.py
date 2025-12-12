from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.pastoral_guidelines.models import PastoralGuidelines
from app.pastoral_guidelines.v1.filters import PastoralGuidelinesFilter
from app.pastoral_guidelines.v1.permissions import PastoralGuidelinesPermission
from app.pastoral_guidelines.v1.serializers import PastoralGuidelinesSerializer


@extend_schema_view(
    retrieve=extend_schema(summary="사목지침 상세 조회"),
)
class PastoralGuidelinesViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = PastoralGuidelines.objects.all()
    serializer_class = PastoralGuidelinesSerializer
    permission_classes = [PastoralGuidelinesPermission]
    pagination_class = CursorPagination
    filterset_class = PastoralGuidelinesFilter
    lookup_url_kwarg = "me"
    lookup_value_regex = "me"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_object(self):
        obj = self.get_queryset().first()
        if not obj:
            raise Http404()
        return obj

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
