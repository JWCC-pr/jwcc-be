from django.db import models
from ordered_model.models import OrderedModel

from app.common.models import BaseModelMixin


class PriestRoleChoices(models.TextChoices):
    PASTOR = "PASTOR", "주임신부"
    ASSOCIATE = "ASSOCIATE", "부주임신부 및 보좌신부"


class PastorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=PriestRoleChoices.PASTOR)


class AssociateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role=PriestRoleChoices.ASSOCIATE)


class Priest(BaseModelMixin, OrderedModel):
    image = models.ImageField(verbose_name="이미지", max_length=1000, upload_to="priest/image/")
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    ordination_date = models.DateField(verbose_name="수품일")

    is_retired = models.BooleanField(verbose_name="퇴임 여부", default=False)

    role = models.CharField(
        verbose_name="직책 구분",
        max_length=10,
        choices=PriestRoleChoices,
        null=True,
        blank=True,
    )

    division = models.CharField(
        verbose_name="구분", max_length=50, blank=True, null=True, help_text="예: 제1대 주임신부"
    )

    assistant_system = models.CharField(
        verbose_name="보좌 체제", max_length=50, blank=True, null=True, help_text="부주임신부에게만 사용"
    )

    start_date = models.DateField(verbose_name="재임 시작일")
    end_date = models.DateField(verbose_name="재임 종료일", blank=True, null=True)

    class Meta:
        db_table = "priest"
        verbose_name = "사제"
        verbose_name_plural = verbose_name
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.baptismal_name})"


class Pastor(Priest):
    objects = PastorManager()

    class Meta:
        proxy = True
        verbose_name = "주임신부"
        verbose_name_plural = verbose_name


class Associate(Priest):
    objects = AssociateManager()

    class Meta:
        proxy = True
        verbose_name = "부주임/보좌신부"
        verbose_name_plural = verbose_name
