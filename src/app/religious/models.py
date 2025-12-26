from django.db import models
from ordered_model.models import OrderedModel
from django.core.exceptions import ValidationError
from app.common.models import BaseModelMixin


class Religious(BaseModelMixin, OrderedModel):
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="religious/image/")
    category = models.CharField(verbose_name="구분", max_length=50, null=True, blank=True)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    start_date = models.DateField(verbose_name="재임 시작일")

    class Meta:
        db_table = "religious"
        verbose_name = "수도자"
        verbose_name_plural = verbose_name
        ordering = ["start_date", "category"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"
