from django.db import models

from app.common.models import BaseModel


class Schedule(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)
    scheduled_at = models.DateField(verbose_name="날짜")
    start_time = models.TimeField(verbose_name="시작시간", help_text="입력하지 않은 경우 하루종일", null=True, blank=True)
    end_time = models.TimeField(verbose_name="종료시간", null=True, blank=True)

    class Meta:
        db_table = "schedule"
        verbose_name = "일정"
        verbose_name_plural = verbose_name
        ordering = ["scheduled_at"]

    def __str__(self):
        return self.title
