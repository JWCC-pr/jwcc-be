from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.room_reservation.models import RepeatRoomReservation, RoomReservation
from app.room_reservation.v1.filters import RoomReservationFilter
from app.room_reservation.v1.permissions import RoomReservationPermission
from app.room_reservation.v1.serializers import RepeatRoomReservationSerializer, RoomReservationSerializer


@extend_schema_view(
    list=extend_schema(summary="교리실 예약 목록 조회"),
    create=extend_schema(summary="교리실 예약 등록"),
    retrieve=extend_schema(summary="교리실 예약 상세 조회"),
    update=extend_schema(summary="교리실 예약 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="교리실 예약 삭제"),
)
class RoomReservationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = RoomReservation.objects.all()
    serializer_class = RoomReservationSerializer
    permission_classes = [RoomReservationPermission]
    pagination_class = LimitOffsetPagination
    filterset_class = RoomReservationFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("room")
        return queryset

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")


@extend_schema_view(
    create=extend_schema(summary="교리실 반복 예약 등록"),
    destroy=extend_schema(summary="교리실 반복 예약 삭제"),
)
class RepeatRoomReservationViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = RepeatRoomReservation.objects.all()
    serializer_class = RepeatRoomReservationSerializer
    permission_classes = [RoomReservationPermission]
