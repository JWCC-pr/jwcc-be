from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view, inline_serializer
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from rest_framework import serializers as drf_serializers

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
                "organization_name": serializer.validated_data.get("organization_name", instance.organization_name),
                "updated_at": timezone.now(),
            }

            RoomReservation.objects.filter(
                repeat_id=instance.repeat_id,
                date__gte=instance.date,
            ).update(**update_fields)

            repeat = instance.repeat
            repeat.title = update_fields["title"]
            repeat.user_name = update_fields["user_name"]
            repeat.organization_name = update_fields["organization_name"]
            repeat.save(update_fields=["title", "user_name", "organization_name", "updated_at"])

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
    create=extend_schema(
        summary="교리실 반복 예약 등록",
        description=(
            "`repeatType=weekly` 사용 시 `weekdays`는 0(월)~6(일) 숫자 배열입니다. "
            "`weekOfMonth`는 1~4주차 지정값이며, 매주 반복이면 `null` 또는 생략합니다. "
            "`repeatType=monthlyDate` 사용 시 `monthDay`를 1~31로 전달합니다."
        ),
        examples=[
            OpenApiExample(
                "요일 반복(매주 월/수)",
                value={
                    "roomId": 1,
                    "title": "초등부 교리",
                    "userName": "홍길동",
                    "organizationName": "초등부",
                    "repeatType": "weekly",
                    "startDate": "2026-03-01",
                    "endDate": "2026-06-30",
                    "startAt": "19:00:00",
                    "endAt": "20:00:00",
                    "weekdays": [0, 2],
                    "weekOfMonth": None,
                    "monthDay": None,
                },
                request_only=True,
            ),
            OpenApiExample(
                "날짜 반복(매월 10일)",
                value={
                    "roomId": 1,
                    "title": "교리봉사자 모임",
                    "userName": "이몽룡",
                    "organizationName": "교리봉사단",
                    "repeatType": "monthlyDate",
                    "startDate": "2026-03-01",
                    "endDate": "2026-12-31",
                    "startAt": "10:00:00",
                    "endAt": "11:00:00",
                    "weekdays": [],
                    "weekOfMonth": None,
                    "monthDay": 10,
                },
                request_only=True,
            ),
        ],
    ),
    update=extend_schema(summary="교리실 반복 예약 수정"),
    partial_update=extend_schema(exclude=True),
    destroy=extend_schema(summary="교리실 반복 예약 삭제"),
)
class RepeatRoomReservationViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = RepeatRoomReservation.objects.all()
    serializer_class = RepeatRoomReservationSerializer
    permission_classes = [RoomReservationPermission]

    def get_queryset(self):
        return super().get_queryset().select_related("room", "created_by")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("patch")


@extend_schema_view(
    list=extend_schema(
        summary="교리실 목록 조회",
        responses=inline_serializer(
            name="CatechismRoomGrouped",
            fields={
                "building": drf_serializers.CharField(),
                "rooms": inline_serializer(
                    name="CatechismRoomItem",
                    fields={
                        "roomId": drf_serializers.IntegerField(),
                        "name": drf_serializers.CharField(),
                        "location": drf_serializers.CharField(),
                    },
                    many=True,
                ),
            },
            many=True,
        ),
    ),
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
    pagination_class = None
    filterset_class = CatechismRoomFilter
    filter_backends = [DjangoFilterBackend]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        grouped = {}
        for room in queryset:
            if room.building not in grouped:
                grouped[room.building] = {
                    "building": room.building,
                    "rooms": [],
                }
            grouped[room.building]["rooms"].append(
                {
                    "roomId": room.id,
                    "name": room.name,
                    "location": room.location,
                }
            )
        return Response(list(grouped.values()))
