from django.db import models

from app.common.models import BaseModel


class WeeklyBulletinEditorialFile(BaseModel):
    weekly_bulletin_editorial = models.ForeignKey(
        "weekly_bulletin_editorial.WeeklyBulletinEditorial",
        verbose_name="주보7면",
        on_delete=models.CASCADE,
        related_name="file_set",
        related_query_name="file",
    )
    file = models.FileField(verbose_name="자료", max_length=1000, upload_to="weekly_bulletin_editorial/file/")

    class Meta:
        app_label = "weekly_bulletin_editorial"
        db_table = "weekly_bulletin_editorial_file"
        verbose_name = "주보7면 파일"
        verbose_name_plural = verbose_name
