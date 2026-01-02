from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from ordered_model.models import OrderedModelManager, OrderedModel

from app.common.models import BaseModel


class WeeklyBulletinEditorialStateChoices(models.IntegerChoices):
    DRAFT = 1, "편집"
    FINAL = 2, "최종본"
    TEMPLATE = 3, "양식"


class WeeklyBulletinEditorialDraftManager(OrderedModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(state=WeeklyBulletinEditorialStateChoices.DRAFT)


class WeeklyBulletinEditorialFinalManager(OrderedModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(state=WeeklyBulletinEditorialStateChoices.FINAL)


class WeeklyBulletinEditorialTemplateManager(OrderedModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(state=WeeklyBulletinEditorialStateChoices.TEMPLATE)


class WeeklyBulletinEditorial(BaseModel, OrderedModel):
    title = models.CharField(verbose_name="제목", max_length=100)
    body = CKEditor5Field(verbose_name="본문")
    state = models.PositiveIntegerField(
        verbose_name="상태",
        choices=WeeklyBulletinEditorialStateChoices,
        default=WeeklyBulletinEditorialStateChoices.DRAFT,
    )

    class Meta:
        db_table = "weekly_bulletin_editorial"
        verbose_name = "주보_7면"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class WeeklyBulletinEditorialDraft(WeeklyBulletinEditorial):
    objects = WeeklyBulletinEditorialDraftManager()

    class Meta:
        proxy = True
        verbose_name = "주보7면 편집본"
        verbose_name_plural = verbose_name


class WeeklyBulletinEditorialFinal(WeeklyBulletinEditorial):
    objects = WeeklyBulletinEditorialFinalManager()

    class Meta:
        proxy = True
        verbose_name = "주보7면 최종본"
        verbose_name_plural = verbose_name


class WeeklyBulletinEditorialTemplate(WeeklyBulletinEditorial):
    objects = WeeklyBulletinEditorialTemplateManager()

    class Meta:
        proxy = True
        verbose_name = "주보7면 양식"
        verbose_name_plural = verbose_name
