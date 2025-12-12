from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class Department(BaseModelMixin, OrderedModel):
    name = models.CharField(verbose_name="분과명", max_length=100)

    class Meta:
        db_table = "department"
        verbose_name = "분과"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return self.name
