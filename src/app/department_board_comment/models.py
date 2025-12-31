from django.db import models

from app.common.models import BaseModel


class DepartmentBoardCommentQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True, body="삭제된 댓글")


class DepartmentBoardCommentManager(models.Manager):
    def get_queryset(self):
        return DepartmentBoardCommentQuerySet(self.model, using=self._db)


class DepartmentBoardComment(BaseModel):
    objects = DepartmentBoardCommentManager()
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    department_board = models.ForeignKey(
        "department_board.DepartmentBoard", verbose_name="분과 게시글", on_delete=models.CASCADE
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="부모 댓글",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_set",
        related_query_name="child",
    )
    body = models.CharField(verbose_name="내용", max_length=500)
    is_modified = models.BooleanField(verbose_name="수정여부", default=False, editable=False)
    is_deleted = models.BooleanField(verbose_name="삭제여부", default=False, editable=False)

    class Meta:
        db_table = "department_board_comment"
        verbose_name = "분과 게시글 댓글"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.body

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.body = "삭제된 댓글"
        self.save(update_fields=["is_deleted", "body"])
        return 0, {}
