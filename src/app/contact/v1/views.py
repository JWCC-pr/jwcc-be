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
    retrieve=extend_schema(summary="Contact 상세 조회"),
)
class ContactViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [ContactPermission]
    pagination_class = CursorPagination
    filterset_class = ContactFilter
    lookup_url_kwarg = "me"
    lookup_value_regex = "me"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_object(self):
        return self.queryset.first()
