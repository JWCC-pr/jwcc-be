from django.db import models

from app.common.models import BaseModel


class DepartmentBoardLike(BaseModel):
    department_board = models.ForeignKey(
        "department_board.DepartmentBoard", verbose_name="분과 게시글", on_delete=models.CASCADE
    )
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)

    class Meta:
        db_table = "department_board_like"
        verbose_name = "분과 게시글 좋아요"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["department_board", "user"], name="unique_department_board_likes"),
        ]
