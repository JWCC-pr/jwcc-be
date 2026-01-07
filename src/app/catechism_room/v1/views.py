from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from app.catechism_room.v1.permissions import CatechismRoomPermission
from app.catechism_room.v1.serializers import CatechismRoomSerializer
from app.catechism_room.models import CatechismRoom


@extend_schema_view(
    list=extend_schema(summary="교리실 목록 조회"),
    retrieve=extend_schema(summary="교리실 상세 조회"),
)
class CatechismRoomViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = CatechismRoom.objects.all()
    serializer_class = CatechismRoomSerializer
    permission_classes = [CatechismRoomPermission]
