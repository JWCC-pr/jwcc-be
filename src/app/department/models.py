from django.db import models

from app.common.models import BaseModel


class Department(BaseModel):
    name = models.CharField(verbose_name="분과명", max_length=100)

    class Meta:
        db_table = "department"
        verbose_name = "분과"
        verbose_name_plural = verbose_name
        ordering = ["name"]

    def __str__(self):
        return self.name
