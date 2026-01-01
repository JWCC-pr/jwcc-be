from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from app.common.models import BaseModel


class DepartmentBoard(BaseModel):
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    department = models.ForeignKey("department.Department", verbose_name="분과", on_delete=models.CASCADE)
    sub_department_set = models.ManyToManyField("department.SubDepartment", verbose_name="세부분과", blank=True)
    title = models.CharField(verbose_name="제목", max_length=100)
    body = CKEditor5Field(verbose_name="본문")

    hit_count = models.PositiveBigIntegerField(verbose_name="조회수", default=0, editable=False)
    comment_count = models.PositiveBigIntegerField(verbose_name="댓글수", default=0, editable=False)
    like_count = models.PositiveBigIntegerField(verbose_name="좋아요수", default=0, editable=False)

    is_modified = models.BooleanField(verbose_name="수정여부", default=False, editable=False)

    class Meta:
        db_table = "department_board"
        verbose_name = "분과 게시글"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
