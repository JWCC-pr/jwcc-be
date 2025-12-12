from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModel, BaseModelMixin


class Banner(BaseModelMixin, OrderedModel):
    name = models.CharField(verbose_name="배너명", max_length=100, help_text="관리용")
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="banner/image/")

    class Meta:
        db_table = "banner"
        verbose_name = "배너"
        verbose_name_plural = verbose_name
        ordering = ["order"]
