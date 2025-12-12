from django.db import models

from app.common.models import BaseModel


class Board(BaseModel):
    class Meta:
        db_table = "board"
        verbose_name = "Board"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
