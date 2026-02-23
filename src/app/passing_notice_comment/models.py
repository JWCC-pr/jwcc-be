from django.db import models

from app.common.models import BaseModel


class PassingNoticeCommentQuerySet(models.QuerySet):
    def delete(self):
        """QuerySet의 delete를 오버라이드하여 소프트 삭제 처리"""
        return self.update(is_deleted=True, body="삭제된 댓글")


class PassingNoticeCommentManager(models.Manager):
    def get_queryset(self):
        return PassingNoticeCommentQuerySet(self.model, using=self._db)


class PassingNoticeComment(BaseModel):
    objects = PassingNoticeCommentManager()
    passing_notice = models.ForeignKey(
        "passing_notice.PassingNotice", verbose_name="선종 안내 댓글", on_delete=models.CASCADE
    )
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.SET_NULL, null=True)
    body = models.CharField(verbose_name="내용", max_length=500)
    is_modified = models.BooleanField(verbose_name="수정여부", default=False, editable=False)
    is_deleted = models.BooleanField(verbose_name="삭제여부", default=False, editable=False)

    class Meta:
        app_label = "passing_notice"
        db_table = "passing_notice_comment"
        verbose_name = "선종 안내 댓글"
        verbose_name_plural = verbose_name
        ordering = ["created_at"]

    def __str__(self):
        return self.body

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.body = "삭제된 댓글"
        self.save(update_fields=["is_deleted", "body"])
        return 0, {}
