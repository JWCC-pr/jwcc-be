from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from app.common.models import BaseModel


class Board(BaseModel):
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=100)
    body = RichTextUploadingField(verbose_name="본문")
    hit_count = models.PositiveBigIntegerField(verbose_name="조회수", default=0, editable=False)
    comment_count = models.PositiveBigIntegerField(verbose_name="댓글수", default=0, editable=False)
    like_count = models.PositiveBigIntegerField(verbose_name="좋아요수", default=0, editable=False)

    class Meta:
        db_table = "board"
        verbose_name = "자유 게시글"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
