from django.db import models

from app.common.models import BaseModel


class DepartmentBoardImage(BaseModel):
    department_board = models.ForeignKey(
        "department_board.DepartmentBoard",
        verbose_name="분과 게시글",
        on_delete=models.CASCADE,
        related_name="image_set",
        related_query_name="image",
    )
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="department_board/image/")

    class Meta:
        app_label = "department_board"
        db_table = "department_board_image"
        verbose_name = "분과 게시글 이미지"
        verbose_name_plural = verbose_name
        ordering = ["created_at"]
