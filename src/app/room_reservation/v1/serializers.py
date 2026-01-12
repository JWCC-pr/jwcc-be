from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db import transaction
from rest_framework import serializers

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
        start_at = attrs.get("start_at") or (self.instance.start_at if self.instance else None)
        end_at = attrs.get("end_at") or (self.instance.end_at if self.instance else None)
        room = attrs.get("room") or (self.instance.room if self.instance else None)
        date = attrs.get("date") or (self.instance.date if self.instance else None)

        if start_at >= end_at:
            raise serializers.ValidationError({"end_at": "종료 시간은 시작 시간 이후여야 합니다."})

        # 겹치는 예약 확인
        qs = RoomReservation.objects.filter(
            room=room,
            date=date,
            start_at__lt=end_at,
            end_at__gt=start_at,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError({"date": "이미 예약된 시간과 겹칩니다."})

        return attrs


class RepeatRoomReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepeatRoomReservation
        fields = "__all__"

    def validate(self, attrs):
        if attrs["start_at"] >= attrs["end_at"]:
            raise serializers.ValidationError({"end_at": "종료 시간은 시작 시간 이후여야 합니다."})

        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError({"end_date": "종료일은 시작일 이후여야 합니다."})

        if attrs["repeat_type"] == RepeatRoomReservation.RepeatType.WEEKLY:
            if not attrs.get("weekdays"):
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
