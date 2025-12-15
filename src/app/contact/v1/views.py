from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination
from app.contact.models import Contact
from app.contact.v1.filters import ContactFilter
from app.contact.v1.permissions import ContactPermission
from app.contact.v1.serializers import ContactSerializer


@extend_schema_view(
    list=extend_schema(summary="Contact 목록 조회"),
    create=extend_schema(summary="Contact 등록"),
    retrieve=extend_schema(summary="Contact 상세 조회"),
    update=extend_schema(summary="Contact 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="Contact 삭제"),
)
class ContactViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [ContactPermission]
    pagination_class = CursorPagination
    filterset_class = ContactFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    # 특정 action에 다른 Filter를 설정해야하는 경우 사용
    def get_filterset_class(self):
        return getattr(self, "filterset_class", None)

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")
