from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class PastorHistory(BaseModelMixin, OrderedModel):
    category = models.CharField(verbose_name="구분", max_length=50)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    start_date = models.DateField(verbose_name="재임 시작일")
    end_date = models.DateField(verbose_name="재임 종료일")

    class Meta:
        db_table = "pastor_history"
        verbose_name = "역대 주임신부"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"
