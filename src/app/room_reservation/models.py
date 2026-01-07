from django.db import models
from rest_framework.exceptions import ValidationError

from app.common.models import BaseModel


class RoomReservation(BaseModel):
    room = models.ForeignKey(
        "catechism_room.CatechismRoom",
        on_delete=models.CASCADE,
        related_name="reservation_set",
        verbose_name="교리실",
    )
    date = models.DateField(verbose_name="예약 날짜")
    start_at = models.TimeField(verbose_name="시작 시간")
    end_at = models.TimeField(verbose_name="종료 시간")

    def clean(self):
        if self.start_at >= self.end_at:
            raise ValidationError("종료 시간은 시작 시간 이후여야 합니다.")

        qs = RoomReservation.objects.filter(
            room=self.room,
        ).exclude(pk=self.pk)

        if qs.filter(
            date=self.date,
            start_at__lt=self.end_at,
            end_at__gt=self.start_at,
        ).exists():
            raise ValidationError("이미 예약된 시간과 겹칩니다.")

    class Meta:
        db_table = "room_reservation"
        verbose_name = "교리실 예약"
        verbose_name_plural = verbose_name
        ordering = ["-date", "-start_at"]

    def __str__(self):
        return f"{self.room.name} - {self.date}"
