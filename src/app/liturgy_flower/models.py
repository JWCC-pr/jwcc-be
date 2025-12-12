from django.db import models

from app.common.models import BaseModel


class LiturgyFlower(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="liturgy_flower/image/")

    class Meta:
        db_table = "liturgy_flower"
        verbose_name = "전례꽃"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
