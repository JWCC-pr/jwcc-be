from django.db import models

from app.common.models import BaseModel


class Document(BaseModel):
    title = models.CharField(verbose_name="제목", max_length=100)

    class Meta:
        db_table = "document"
        verbose_name = "자료"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
