from django.db import models

from app.common.models import BaseModel


class NoticeFile(BaseModel):
    notice = models.ForeignKey(
        "notice.Notice",
        verbose_name="공지사항",
        on_delete=models.CASCADE,
        related_name="file_set",
        related_query_name="file",
    )
    file = models.FileField(verbose_name="파일", max_length=1000, upload_to="notice/file/")

    class Meta:
        app_label = "notice"
        db_table = "notice_file"
        verbose_name = "공지사항 파일"
        verbose_name_plural = verbose_name
