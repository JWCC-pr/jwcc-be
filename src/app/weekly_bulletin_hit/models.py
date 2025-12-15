from django.db import models

from app.common.models import BaseModel


class WeeklyBulletinHit(BaseModel):
    weekly_bulletin = models.ForeignKey(
        "weekly_bulletin.WeeklyBulletin", verbose_name="자유 게시글", on_delete=models.CASCADE
    )
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소", null=True, blank=True)

    class Meta:
        db_table = "weekly_bulletin_hit"
        verbose_name = "주보 조회"
        verbose_name_plural = verbose_name
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["weekly_bulletin", "user"], name="unique_weekly_bulletin_user_hit"),
            models.UniqueConstraint(fields=["weekly_bulletin", "ip_address"], name="unique_weekly_bulletin_ip_hit"),
        ]
