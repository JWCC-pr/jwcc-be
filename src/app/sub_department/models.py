from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModel


class SubDepartment(BaseModel, OrderedModel):
    department = models.ForeignKey(
        "department.Department",
        verbose_name="분과",
        on_delete=models.CASCADE,
        related_name="sub_department_set",
        related_query_name="sub_department",
    )
    name = models.CharField(verbose_name="세부분과명", max_length=100)
    order_with_respect_to = "department"

    class Meta(OrderedModel.Meta):
        app_label = "department"
        db_table = "sub_department"
        verbose_name = "세부분과"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return self.name
