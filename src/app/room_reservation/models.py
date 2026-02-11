from django.db import models
from rest_framework.exceptions import ValidationError

from app.common.models import BaseModel


def _validate_half_hour_interval(start_at, end_at):
    if start_at is None or end_at is None:
        return

    if start_at >= end_at:
        raise ValidationError("종료 시간은 시작 시간 이후여야 합니다.")

    if start_at.minute not in {0, 30} or end_at.minute not in {0, 30}:
        raise ValidationError("예약 시간은 30분 단위여야 합니다.")


class CatechismRoom(BaseModel):
    name = models.CharField("교리실명", max_length=50)
    location = models.TextField("위치", blank=True, default="")
    building = models.CharField("건물명", max_length=50, blank=True, default="")

    class Meta:
        db_table = "catechism_room"
        verbose_name = "교리실"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class RepeatRoomReservation(BaseModel):
    class RepeatType(models.TextChoices):
        WEEKLY = "weekly", "요일 반복"
        MONTHLY_DATE = "monthly_date", "날짜 반복"

    room = models.ForeignKey(
        "room_reservation.CatechismRoom",
        on_delete=models.CASCADE,
        related_name="repeat_reservation_set",
        verbose_name="교리실",
    )
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="repeat_room_reservation_set",
        verbose_name="예약 생성자",
        null=True,
        blank=True,
    )
    title = models.CharField(verbose_name="예약 제목", max_length=50)
    user_name = models.CharField(verbose_name="사용자명", max_length=10, default="")
    organization_name = models.CharField(verbose_name="사용단체명", max_length=50, blank=True, default="")
    repeat_type = models.CharField(
        verbose_name="반복 유형",
        max_length=20,
        choices=RepeatType.choices,
    )
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일")
    start_at = models.TimeField(verbose_name="시작 시간")
    end_at = models.TimeField(verbose_name="종료 시간")
    weekdays = models.JSONField(verbose_name="반복 요일", default=list, blank=True)
    week_of_month = models.PositiveSmallIntegerField(verbose_name="반복 주차", null=True, blank=True)
    month_day = models.PositiveSmallIntegerField(verbose_name="반복 일자", null=True, blank=True)

    class Meta:
        db_table = "repeat_room_reservation"
        verbose_name = "반복 예약"
        verbose_name_plural = verbose_name

    def clean(self):
        _validate_half_hour_interval(self.start_at, self.end_at)

        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("시작일은 종료일 이전이어야 합니다.")

        if self.repeat_type == self.RepeatType.WEEKLY:
            if not self.weekdays:
                raise ValidationError("요일 반복 시 요일을 선택해야 합니다.")
            if self.week_of_month and self.week_of_month not in {1, 2, 3, 4}:
                raise ValidationError("반복 주차는 1~4주차만 가능합니다.")
            if self.month_day:
                raise ValidationError("요일 반복과 날짜 반복을 동시에 사용할 수 없습니다.")

        if self.repeat_type == self.RepeatType.MONTHLY_DATE:
            if not self.month_day:
                raise ValidationError("날짜 반복 시 반복 일자를 입력해야 합니다.")
            if self.month_day < 1 or self.month_day > 31:
                raise ValidationError("반복 일자는 1~31 사이여야 합니다.")
            if self.weekdays or self.week_of_month:
                raise ValidationError("요일 반복과 날짜 반복을 동시에 사용할 수 없습니다.")

    def __str__(self):
        return f"{self.room.name} - {self.title} ({self.get_repeat_type_display()})"


class RoomReservation(BaseModel):
    room = models.ForeignKey(
        "room_reservation.CatechismRoom",
        on_delete=models.CASCADE,
        related_name="reservation_set",
        verbose_name="교리실",
    )
    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="room_reservation_set",
        verbose_name="예약 생성자",
        null=True,
        blank=True,
    )
    repeat = models.ForeignKey(
        "RepeatRoomReservation",
        on_delete=models.CASCADE,
        related_name="reservation_set",
        verbose_name="반복 예약",
        null=True,
        blank=True,
    )
    title = models.CharField(verbose_name="예약 제목", max_length=50)
    user_name = models.CharField(verbose_name="사용자명", max_length=10, default="")
    organization_name = models.CharField(verbose_name="사용단체명", max_length=50, blank=True, default="")
    date = models.DateField(verbose_name="예약 날짜")
    start_at = models.TimeField(verbose_name="시작 시간")
    end_at = models.TimeField(verbose_name="종료 시간")

    def clean(self):
        _validate_half_hour_interval(self.start_at, self.end_at)

        qs = RoomReservation.objects.filter(
            room=self.room,
            date=self.date,
            start_at__lt=self.end_at,
            end_at__gt=self.start_at,
        ).exclude(pk=self.pk)

        if qs.exists():
            raise ValidationError(f"{self.date} 에 이미 예약된 시간과 겹칩니다.")

    class Meta:
        db_table = "room_reservation"
        verbose_name = "교리실 예약"
        verbose_name_plural = verbose_name
        ordering = ["-date", "-start_at"]

    def __str__(self):
        return f"{self.room.name} - {self.title} ({self.date})"
