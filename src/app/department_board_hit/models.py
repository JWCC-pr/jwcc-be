from django.db import models

from app.common.models import BaseModel


class DepartmentBoardHit(BaseModel):
    department_board = models.ForeignKey(
        "department_board.DepartmentBoard", verbose_name="분과 게시글", on_delete=models.CASCADE
    )
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField(verbose_name="IP 주소", null=True, blank=True)

    class Meta:
        db_table = "department_board_hit"
        verbose_name = "분과 게시글 조회"
        verbose_name_plural = verbose_name
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["department_board", "user"], name="unique_department_board_user_hit"),
            models.UniqueConstraint(fields=["department_board", "ip_address"], name="unique_department_board_ip_hit"),
        ]
