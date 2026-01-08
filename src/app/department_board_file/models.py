from django.db import models

from app.common.models import BaseModel
from app.common.storages import DownloadableMediaStorage


class DepartmentBoardFile(BaseModel):
    department_board = models.ForeignKey(
        "department_board.DepartmentBoard",
        verbose_name="분과 게시글",
        on_delete=models.CASCADE,
        related_name="file_set",
        related_query_name="file",
    )
    file = models.FileField(
        verbose_name="분과게시글 파일",
        max_length=1000,
        upload_to="department_board/file/",
        storage=DownloadableMediaStorage(),
    )

    class Meta:
        app_label = "department_board"
        db_table = "department_board_file"
        verbose_name = "분과 게시글 파일"
        verbose_name_plural = verbose_name
        ordering = ["created_at"]
