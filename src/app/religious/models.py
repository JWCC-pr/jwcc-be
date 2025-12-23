from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class Religious(BaseModelMixin, OrderedModel):
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="religious/image/")
    category = models.CharField(verbose_name="구분", max_length=50)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    start_date = models.DateField(verbose_name="재임 시작일")

    is_retired = models.BooleanField(verbose_name="퇴임 여부", default=False)
    end_date = models.DateField(verbose_name="재임 종료일", null=True, blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.is_retired and not self.end_date:
            raise ValidationError({"end_date": "퇴임 시 재임 종료일을 입력해야 합니다."})

    class Meta:
        db_table = "religious"
        verbose_name = "수도자"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"
