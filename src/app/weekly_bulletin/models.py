from django.db import models

from app.common.models import BaseModel
from app.common.storages import DownloadableMediaStorage


class WeeklyBulletin(BaseModel):
    thumbnail = models.ImageField(verbose_name="썸네일", max_length=1000, upload_to="weekly_bulletin/thumbnail/")
    title = models.CharField(verbose_name="제목", max_length=100)
    file = models.FileField(
        verbose_name="주보 파일",
        max_length=1000,
        upload_to="weekly_bulletin/file/",
        storage=DownloadableMediaStorage(),
    )
    hit_count = models.PositiveBigIntegerField(verbose_name="조회수", default=0, editable=False)

    class Meta:
        db_table = "weekly_bulletin"
        verbose_name = "주보"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
