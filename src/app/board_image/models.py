from django.db import models

from app.common.models import BaseModel


class BoardImage(BaseModel):
    board = models.ForeignKey(
        "board.Board",
        verbose_name="자유 게시글",
        on_delete=models.CASCADE,
        related_name="image_set",
        related_query_name="image",
    )
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="board/image/")

    class Meta:
        app_label = "board"
        db_table = "board_image"
        verbose_name = "자유 게시글 이미지"
        verbose_name_plural = verbose_name
        ordering = ["created_at"]
