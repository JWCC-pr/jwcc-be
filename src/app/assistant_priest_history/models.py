from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class AssistantPriestHistory(BaseModelMixin, OrderedModel):
    assistant_system = models.CharField(verbose_name="보좌 체제", max_length=50)
    category = models.CharField(verbose_name="구분", max_length=50)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    start_date = models.DateField(verbose_name="재임 시작일")
    end_date = models.DateField(verbose_name="재임 종료일")

    class Meta:
        db_table = "assistant_priest_history"
        verbose_name = "역대 부주임/보좌신부"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"
