from django.db import models

from app.common.models import BaseModel


class LiturgyFlower(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)

    class Meta:
        db_table = "liturgy_flower"
        verbose_name = "전례꽃"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
