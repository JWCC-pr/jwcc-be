from django.db import models

from app.common.models import BaseModel


class BoardLike(BaseModel):
    board = models.ForeignKey("board.Board", verbose_name="자유 게시글", on_delete=models.CASCADE)
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)

    class Meta:
        db_table = "board_like"
        verbose_name = "자유 게시글 좋아요"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["board", "user"], name="unique_board_likes"),
        ]
