from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from app.common.models import BaseModel


class News(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)
    thumbnail = models.ImageField(verbose_name="썸네일", max_length=1000, upload_to="news/thumbnail/")
    body = CKEditor5Field(verbose_name="본문", config_name="media")
    is_public = models.BooleanField(verbose_name="전체공개", default=True)

    class Meta:
        db_table = "news"
        verbose_name = "본당소식"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
