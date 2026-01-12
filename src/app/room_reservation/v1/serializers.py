from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.room_reservation.models import RepeatRoomReservation, RoomReservation


class RoomReservationSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = RoomReservation
        fields = [
            "id",
            "room",
            "room_name",
            "repeat",
            "title",
            "date",
            "start_at",
            "end_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["repeat"]

    def validate(self, attrs):
        instance = self.instance or RoomReservation()
        instance.room = attrs.get("room", getattr(instance, "room", None))
        instance.date = attrs.get("date", getattr(instance, "date", None))
        instance.start_at = attrs.get("start_at", getattr(instance, "start_at", None))
        instance.end_at = attrs.get("end_at", getattr(instance, "end_at", None))

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict if hasattr(e, "message_dict") else e.messages)

        return attrs


class RepeatRoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatRoomReservation
        fields = "id", "room", "title", "start_at", "end_at", "start_date", "end_date", "repeat_type", "weekdays"

    def validate(self, attrs):
        instance = self.instance or RepeatRoomReservation()

        instance.start_at = attrs.get("start_at", instance.start_at)
        instance.end_at = attrs.get("end_at", instance.end_at)
        instance.start_date = attrs.get("start_date", instance.start_date)
        instance.end_date = attrs.get("end_date", instance.end_date)
        instance.repeat_type = attrs.get("repeat_type", instance.repeat_type)
        instance.weekdays = attrs.get("weekdays", instance.weekdays)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict or e.messages)

        if instance.repeat_type == RepeatRoomReservation.RepeatType.WEEKLY and not instance.weekdays:
            raise serializers.ValidationError({"weekdays": "매주 반복 시 요일을 선택해야 합니다."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        repeat = RepeatRoomReservation.objects.create(**validated_data)

        reservations = []
        current = repeat.start_date

        while current <= repeat.end_date:
            should_create = False

            if repeat.repeat_type == RepeatRoomReservation.RepeatType.DAILY:
                should_create = True

            elif repeat.repeat_type == RepeatRoomReservation.RepeatType.WEEKLY:
                if current.weekday() in repeat.weekdays:
                    should_create = True

            elif repeat.repeat_type == RepeatRoomReservation.RepeatType.MONTHLY:
                if current.day == repeat.start_date.day:
                    should_create = True

            if should_create:
                reservation = RoomReservation(
                    room=repeat.room,
                    title=repeat.title,
                    date=current,
                    start_at=repeat.start_at,
                    end_at=repeat.end_at,
                    repeat=repeat,
                )
                # 기존 단일 예약 검증 로직 재사용
                reservation.clean()
                reservations.append(reservation)

            # 날짜 증가
            if repeat.repeat_type == RepeatRoomReservation.RepeatType.MONTHLY:
                current += relativedelta(months=1)
            else:
                current += timedelta(days=1)

        RoomReservation.objects.bulk_create(reservations)
        return repeat
