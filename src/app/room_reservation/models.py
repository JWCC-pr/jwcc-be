from django.db import models
from rest_framework.exceptions import ValidationError

from app.common.models import BaseModel


class RepeatRoomReservation(BaseModel):
    class RepeatType(models.TextChoices):
        DAILY = "daily", "매일"
        WEEKLY = "weekly", "매주"
        MONTHLY = "monthly", "매월"

    room = models.ForeignKey(
        "catechism_room.CatechismRoom",
        on_delete=models.CASCADE,
        related_name="repeat_reservation_set",
        verbose_name="교리실",
    )
    title = models.CharField(verbose_name="예약 제목", max_length=100)
    repeat_type = models.CharField(
        verbose_name="반복 유형",
        max_length=10,
        choices=RepeatType.choices,
    )
    start_date = models.DateField(verbose_name="시작일")
    end_date = models.DateField(verbose_name="종료일")
    start_at = models.TimeField(verbose_name="시작 시간")
    end_at = models.TimeField(verbose_name="종료 시간")
    weekdays = models.JSONField(verbose_name="반복 요일", default=list, blank=True)

    class Meta:
        db_table = "repeat_room_reservation"
        verbose_name = "반복 예약"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.room.name} - {self.title} ({self.get_repeat_type_display()})"


class RoomReservation(BaseModel):
    room = models.ForeignKey(
        "catechism_room.CatechismRoom",
        on_delete=models.CASCADE,
        related_name="reservation_set",
        verbose_name="교리실",
    )
    repeat = models.ForeignKey(
        "RepeatRoomReservation",
        on_delete=models.CASCADE,
        related_name="reservation_set",
        verbose_name="반복 예약",
        null=True,
        blank=True,
    )
    title = models.CharField(verbose_name="예약 제목", max_length=100)
    date = models.DateField(verbose_name="예약 날짜")
    start_at = models.TimeField(verbose_name="시작 시간")
    end_at = models.TimeField(verbose_name="종료 시간")

    def clean(self):
        if self.start_at >= self.end_at:
            raise ValidationError("종료 시간은 시작 시간 이후여야 합니다.")

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
