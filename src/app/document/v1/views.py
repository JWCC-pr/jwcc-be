from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.document.models import Document
from app.document.v1.filters import DocumentFilter
from app.document.v1.permissions import DocumentPermission
from app.document.v1.serializers import DocumentSerializer


@extend_schema_view(
    list=extend_schema(summary="자료 목록 조회"),
    retrieve=extend_schema(summary="자료 상세 조회"),
)
class DocumentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [DocumentPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = DocumentFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
