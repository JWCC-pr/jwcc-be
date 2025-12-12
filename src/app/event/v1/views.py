from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import CursorPagination, LimitOffsetPagination
from app.event.models import Event
from app.event.v1.filters import EventFilter
from app.event.v1.permissions import EventPermission
from app.event.v1.serializers import EventSerializer


@extend_schema_view(
    list=extend_schema(summary="행사 목록 조회"),
    retrieve=extend_schema(summary="행사 상세 조회"),
)
class EventViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [EventPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = EventFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
