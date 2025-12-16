from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from app.common.models import BaseModel


class Event(BaseModel):
    thumbnail = models.ImageField(verbose_name="썸네일", max_length=1000, upload_to="event/thumbnail/")
    title = models.CharField(verbose_name="제목", max_length=100)
    body = CKEditor5Field(verbose_name="본문")
    youtube_link = models.URLField(verbose_name="유튜브 링크", max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "event"
        verbose_name = "행사"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
