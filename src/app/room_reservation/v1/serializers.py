import calendar
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.room_reservation.models import CatechismRoom, RepeatRoomReservation, RoomReservation
from app.room_reservation.v1.utils import find_conflicts


def iter_month_starts(start_date, end_date):
    current = date(start_date.year, start_date.month, 1)
    while current <= end_date:
        yield current
        current += relativedelta(months=1)


def generate_repeat_dates(repeat):
    dates = []

    if repeat.repeat_type == RepeatRoomReservation.RepeatType.WEEKLY:
        if repeat.week_of_month:
            for month_start in iter_month_starts(repeat.start_date, repeat.end_date):
                month_calendar = calendar.monthcalendar(month_start.year, month_start.month)
                for weekday in repeat.weekdays:
                    occurrences = [week[weekday] for week in month_calendar if week[weekday] != 0]
                    for wom in repeat.week_of_month:
                        if wom <= len(occurrences):
                            day = occurrences[wom - 1]
                            candidate = date(month_start.year, month_start.month, day)
                            if repeat.start_date <= candidate <= repeat.end_date:
                                dates.append(candidate)
        else:
            current = repeat.start_date
            while current <= repeat.end_date:
                if current.weekday() in repeat.weekdays:
                    dates.append(current)
                current += timedelta(days=1)

    if repeat.repeat_type == RepeatRoomReservation.RepeatType.MONTHLY_DATE:
        for month_start in iter_month_starts(repeat.start_date, repeat.end_date):
            last_day = calendar.monthrange(month_start.year, month_start.month)[1]
            if repeat.month_day <= last_day:
                candidate = date(month_start.year, month_start.month, repeat.month_day)
                if repeat.start_date <= candidate <= repeat.end_date:
                    dates.append(candidate)

    return sorted(set(dates))


class CatechismRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatechismRoom
        fields = [
            "id",
            "name",
            "location",
            "building",
            "created_at",
            "updated_at",
        ]


class RoomReservationSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source="room", queryset=CatechismRoom.objects.all())
    room_name = serializers.CharField(source="room.name", read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_name = serializers.CharField(source="created_by.name", read_only=True)

    repeat_id = serializers.PrimaryKeyRelatedField(source="repeat", read_only=True)

    class Meta:
        model = RoomReservation
        fields = [
            "id",
            "room_id",
            "room_name",
            "repeat_id",
            "title",
            "user_name",
            "organization_name",
            "date",
            "start_at",
            "end_at",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["repeat_id", "created_by", "created_by_name"]

    def validate(self, attrs):
        instance = self.instance or RoomReservation()
        instance.room = attrs.get("room", getattr(instance, "room", None))
        instance.date = attrs.get("date", getattr(instance, "date", None))
        instance.start_at = attrs.get("start_at", getattr(instance, "start_at", None))
        instance.end_at = attrs.get("end_at", getattr(instance, "end_at", None))

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["created_by"] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.room = validated_data.get("room", instance.room)
        instance.title = validated_data.get("title", instance.title)
        instance.user_name = validated_data.get("user_name", instance.user_name)
        instance.organization_name = validated_data.get("organization_name", instance.organization_name)
        instance.date = validated_data.get("date", instance.date)
        instance.start_at = validated_data.get("start_at", instance.start_at)
        instance.end_at = validated_data.get("end_at", instance.end_at)
        instance.save(
            update_fields=[
                "room",
                "title",
                "user_name",
                "organization_name",
                "date",
                "start_at",
                "end_at",
                "updated_at",
            ]
        )
        return instance


class RepeatRoomReservationSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(source="room", queryset=CatechismRoom.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_name = serializers.CharField(source="created_by.name", read_only=True)
    weekdays = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=6),
        required=False,
        allow_empty=True,
        help_text="요일 반복 값. 0=월, 1=화, 2=수, 3=목, 4=금, 5=토, 6=일",
    )
    week_of_month = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=4),
        required=False,
        allow_empty=True,
        help_text="월별 n주차 반복에서만 사용합니다. 복수 선택 가능(예: [1, 3]). 매주 반복이면 [] 또는 생략하세요.",
    )
    month_day = serializers.IntegerField(
        required=False,
        allow_null=True,
        min_value=1,
        max_value=31,
        help_text="날짜 반복(monthlyDate)일 때 사용할 일자(1~31)",
    )

    class Meta:
        model = RepeatRoomReservation
        fields = [
            "id",
            "room_id",
            "title",
            "user_name",
            "organization_name",
            "repeat_type",
            "start_date",
            "end_date",
            "start_at",
            "end_at",
            "weekdays",
            "week_of_month",
            "month_day",
            "created_by",
            "created_by_name",
        ]
        read_only_fields = ["created_by", "created_by_name"]

    def validate(self, attrs):
        instance = self.instance or RepeatRoomReservation()

        instance.room = attrs.get("room", getattr(instance, "room", None))
        instance.title = attrs.get("title", instance.title)
        instance.user_name = attrs.get("user_name", instance.user_name)
        instance.repeat_type = attrs.get("repeat_type", instance.repeat_type)
        instance.start_date = attrs.get("start_date", instance.start_date)
        instance.end_date = attrs.get("end_date", instance.end_date)
        instance.start_at = attrs.get("start_at", instance.start_at)
        instance.end_at = attrs.get("end_at", instance.end_at)
        instance.weekdays = attrs.get("weekdays", instance.weekdays)
        instance.week_of_month = attrs.get("week_of_month", instance.week_of_month)
        instance.month_day = attrs.get("month_day", instance.month_day)

        try:
            instance.clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.detail)

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["created_by"] = request.user

        repeat = RepeatRoomReservation(**validated_data)

        dates = generate_repeat_dates(repeat)
        if not dates:
            raise serializers.ValidationError({"detail": "반복 일정이 생성되지 않았습니다."})

        find_conflicts(
            room=repeat.room,
            start_at=repeat.start_at,
            end_at=repeat.end_at,
            dates=dates,
        )

        repeat.save()
        reservations = [
            RoomReservation(
                room=repeat.room,
                title=repeat.title,
                user_name=repeat.user_name,
                organization_name=repeat.organization_name,
                date=reservation_date,
                start_at=repeat.start_at,
                end_at=repeat.end_at,
                repeat=repeat,
                created_by=repeat.created_by,
            )
            for reservation_date in dates
        ]

        RoomReservation.objects.bulk_create(reservations)
        return repeat

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. 기존 개별 예약 삭제
        instance.reservation_set.all().delete()

        # 2. RepeatRoomReservation 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # 3. 새 날짜 생성
        dates = generate_repeat_dates(instance)
        if not dates:
            raise serializers.ValidationError({"detail": "반복 일정이 생성되지 않았습니다."})

        # 4. 충돌 검사 (기존 예약은 이미 삭제했지만 안전장치로 exclude_repeat_id 사용)
        find_conflicts(
            room=instance.room,
            start_at=instance.start_at,
            end_at=instance.end_at,
            dates=dates,
            exclude_repeat_id=instance.pk,
        )

        # 5. 저장 및 개별 예약 재생성
        instance.save()
        reservations = [
            RoomReservation(
                room=instance.room,
                title=instance.title,
                user_name=instance.user_name,
                organization_name=instance.organization_name,
                date=reservation_date,
                start_at=instance.start_at,
                end_at=instance.end_at,
                repeat=instance,
                created_by=instance.created_by,
            )
            for reservation_date in dates
        ]
        RoomReservation.objects.bulk_create(reservations)
        return instance
