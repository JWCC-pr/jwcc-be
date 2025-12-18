from django.db import models

from app.common.models import BaseModel


class LiturgyFlowerImage(BaseModel):
    liturgy_flower = models.ForeignKey(
        "liturgy_flower.LiturgyFlower",
        verbose_name="전례꽃",
        on_delete=models.CASCADE,
        related_name="image_set",
        related_query_name="image",
    )
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="liturgy_flower/image/")

    class Meta:
        app_label = "liturgy_flower"
        db_table = "liturgy_flower_image"
        verbose_name = "이미지"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
