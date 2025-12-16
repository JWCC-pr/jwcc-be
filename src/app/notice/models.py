from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from app.common.models import BaseModel


class Notice(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)
    body = CKEditor5Field(verbose_name="본문")

    class Meta:
        db_table = "notice"
        verbose_name = "공지사항"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
