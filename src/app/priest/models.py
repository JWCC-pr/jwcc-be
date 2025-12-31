from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class Priest(BaseModelMixin, OrderedModel):
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="priest/image/")
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    ordination_date = models.DateField(verbose_name="수품일")
    start_date = models.DateField(verbose_name="재임 시작일")

    class Meta:
        db_table = "priest"
        verbose_name = "사제"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"
