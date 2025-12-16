from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from app.common.models import BaseModel


class PastoralGuidelines(BaseModel):
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="pastoral_guideline/image/")
    title = models.CharField(verbose_name="제목", max_length=100)
    subtitle = models.CharField(verbose_name="서브 제목", max_length=500)
    body = CKEditor5Field(verbose_name="내용")

    class Meta:
        db_table = "pastoral_guidelines"
        verbose_name = "사목지침"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
