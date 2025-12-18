from django.db import models

from app.common.models import BaseModel


class LiturgyFlower(BaseModel):
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=100)
    comment_count = models.PositiveBigIntegerField(verbose_name="댓글수", default=0, editable=False)
    '''
    hit_count = models.PositiveBigIntegerField(verbose_name="조회수", default=0, editable=False)
    like_count = models.PositiveBigIntegerField(verbose_name="좋아요수", default=0, editable=False)
    '''

    class Meta:
        db_table = "liturgy_flower"
        verbose_name = "전례꽃"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
