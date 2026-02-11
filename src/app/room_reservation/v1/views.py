from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.common.pagination import LimitOffsetPagination
from app.room_reservation.models import CatechismRoom, RepeatRoomReservation, RoomReservation
from app.room_reservation.v1.filters import CatechismRoomFilter, RoomReservationFilter
from app.room_reservation.v1.permissions import CatechismRoomPermission, RoomReservationPermission
from app.room_reservation.v1.serializers import (
    CatechismRoomSerializer,
    RepeatRoomReservationSerializer,
    RoomReservationSerializer,
)


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
        queryset = queryset.select_related("room", "created_by", "repeat")
        return queryset

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")

    def update(self, request, *args, **kwargs):
        scope = request.query_params.get("scope")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if scope == "all" and instance.repeat_id:
            update_fields = {
                "title": serializer.validated_data.get("title", instance.title),
                "user_name": serializer.validated_data.get("user_name", instance.user_name),
                "updated_at": timezone.now(),
            }

            RoomReservation.objects.filter(
                repeat_id=instance.repeat_id,
                date__gte=instance.date,
            ).update(**update_fields)

            repeat = instance.repeat
            repeat.title = update_fields["title"]
            repeat.user_name = update_fields["user_name"]
            repeat.save(update_fields=["title", "user_name", "updated_at"])

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        scope = request.query_params.get("scope")
        instance = self.get_object()

        if scope == "all" and instance.repeat_id:
            repeat_id = instance.repeat_id
            RoomReservation.objects.filter(
                repeat_id=repeat_id,
                date__gte=instance.date,
            ).delete()

            if not RoomReservation.objects.filter(repeat_id=repeat_id).exists():
                RepeatRoomReservation.objects.filter(id=repeat_id).delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        return super().destroy(request, *args, **kwargs)


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

    def get_queryset(self):
        return super().get_queryset().select_related("room", "created_by")


@extend_schema_view(
    list=extend_schema(summary="교리실 목록 조회"),
    create=extend_schema(summary="교리실 등록"),
    retrieve=extend_schema(summary="교리실 상세 조회"),
    update=extend_schema(summary="교리실 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="교리실 삭제"),
)
class CatechismRoomViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = CatechismRoom.objects.all()
    serializer_class = CatechismRoomSerializer
    permission_classes = [CatechismRoomPermission]
    filterset_class = CatechismRoomFilter
    filter_backends = [DjangoFilterBackend]
