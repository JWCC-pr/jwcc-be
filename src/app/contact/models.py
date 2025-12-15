from django.db import models

from app.common.models import BaseModel


class Contact(BaseModel):
    office_phone = models.CharField(verbose_name="사무실 연락처", max_length=13)
    president_name = models.CharField(verbose_name="연령회장 이름", max_length=40)
    president_phone = models.CharField(verbose_name="연령회장 연락처", max_length=13)

    class Meta:
        db_table = "contact"
        verbose_name = "연락처"
        verbose_name_plural = verbose_name
