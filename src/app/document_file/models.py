from django.db import models

from app.common.models import BaseModel
from app.common.storages import DownloadableMediaStorage


class DocumentFile(BaseModel):
    document = models.ForeignKey(
        "document.Document",
        verbose_name="자료",
        on_delete=models.CASCADE,
        related_name="file_set",
        related_query_name="file",
    )
    file = models.FileField(
        verbose_name="자료",
        max_length=1000,
        upload_to="document/file/",
        storage=DownloadableMediaStorage(),
    )

    class Meta:
        app_label = "document"
        db_table = "document_file"
        verbose_name = "파일"
        verbose_name_plural = verbose_name
