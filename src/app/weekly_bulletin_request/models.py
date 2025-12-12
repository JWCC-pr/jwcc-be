from django.db import models

from app.common.models import BaseModel


class WeeklyBulletinRequest(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=100)
    file = models.FileField(verbose_name="주보 파일", max_length=1000, upload_to="weekly_bulletin/file/")

    class Meta:
        app_label = "weekly_bulletin"
        db_table = "weekly_bulletin_request"
        verbose_name = "주보 원고 접수"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
