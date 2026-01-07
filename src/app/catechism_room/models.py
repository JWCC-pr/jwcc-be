from django.db import models

from app.common.models import BaseModel


class CatechismRoom(BaseModel):
    name = models.CharField("교리실명", max_length=50)
    location = models.TextField("위치", blank=True, default="")
    description = models.TextField("설명", blank=True, default="")

    class Meta:
        db_table = "catechism_room"
        verbose_name = "교리실"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
