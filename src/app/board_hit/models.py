from django.db import models

from app.common.models import BaseModel


class BoardHit(BaseModel):
    board = models.ForeignKey("board.Board", verbose_name="자유 게시글", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소", null=True, blank=True)

    class Meta:
        db_table = "board_hit"
        verbose_name = "자유 게시글 조회"
        verbose_name_plural = verbose_name
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["board", "user"], name="unique_user_hit"),
            models.UniqueConstraint(fields=["board", "ip_address"], name="unique_ip_hit"),
        ]
