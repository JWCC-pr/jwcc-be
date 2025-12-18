from django.db import models

from app.common.models import BaseModel


class LiturgyFlowerHit(BaseModel):
    liturgy_flower = models.ForeignKey("liturgy_flower.LiturgyFlower", verbose_name="전례꽃", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소", null=True, blank=True)

    class Meta:
        db_table = "liturgy_flower_hit"
        verbose_name = "전례꽃 조회"
        verbose_name_plural = verbose_name
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["liturgy_flower", "user"], name="unique_liturgy_flower_user_hit"),
            models.UniqueConstraint(fields=["liturgy_flower", "ip_address"], name="unique_liturgy_flower_ip_hit"),
        ]
