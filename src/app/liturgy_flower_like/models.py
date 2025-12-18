from django.db import models

from app.common.models import BaseModel


class LiturgyFlowerLike(BaseModel):
    liturgy_flower = models.ForeignKey("liturgy_flower.LiturgyFlower", verbose_name="전례꽃", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)

    class Meta:
        db_table = "liturgy_flower_like"
        verbose_name = "전례꽃 좋아요"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["liturgy_flower", "user"], name="unique_liturgy_flower_likes"),
        ]
