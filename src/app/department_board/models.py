from django.core.exceptions import ValidationError
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from app.common.models import BaseModel


class DepartmentBoard(BaseModel):
    user = models.ForeignKey("user.User", verbose_name="유저", on_delete=models.CASCADE)
    department = models.ForeignKey("department.Department", verbose_name="분과", on_delete=models.CASCADE)
    sub_department = models.ForeignKey("department.SubDepartment", verbose_name="세부분과", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="제목", max_length=100)
    body = CKEditor5Field(verbose_name="본문")

    hit_count = models.PositiveBigIntegerField(verbose_name="조회수", default=0, editable=False)
    comment_count = models.PositiveBigIntegerField(verbose_name="댓글수", default=0, editable=False)
    like_count = models.PositiveBigIntegerField(verbose_name="좋아요수", default=0, editable=False)

    is_modified = models.BooleanField(verbose_name="수정여부", default=False, editable=False)
    is_pinned = models.BooleanField(verbose_name="고정 여부", default=False)
    is_secret = models.BooleanField(verbose_name="비공개 여부", default=False)

    class Meta:
        db_table = "department_board"
        verbose_name = "분과 게시글"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def clean(self):
        if not self.is_pinned:
            return

        department_id = self.department_id
        if not department_id:
            return

        qs = DepartmentBoard.objects.filter(department_id=department_id, is_pinned=True)
        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if qs.count() >= 5:
            raise ValidationError("분과별 고정 게시글은 최대 5개까지 등록할 수 있습니다.")

    def __str__(self):
        return self.title
