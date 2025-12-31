from django.db import models

from app.common.models import BaseModel


class PassingNotice(BaseModel):
    portrait = models.ImageField(verbose_name="고인 사진", max_length=1000, upload_to="passing_notice/portrait/")
    name = models.CharField(verbose_name="고인 성함", max_length=20)
    baptismal_name = models.CharField(verbose_name="고인 세례명", max_length=40)
    age = models.PositiveIntegerField(verbose_name="고인 나이")
    passing_at = models.DateTimeField(verbose_name="선종일시")
    funeral_start_at = models.DateField(verbose_name="장례 시작일")
    funeral_end_at = models.DateField(verbose_name="장례 종료일")
    funeral_mass_at = models.DateField(verbose_name="장례미사 일정")
    funeral_mass_location = models.CharField(verbose_name="장례미사 장소", max_length=200)
    funeral_hall_address = models.CharField(verbose_name="빈소 위치", max_length=200)
    chief_mourner = models.CharField(verbose_name="상주")
    encoffinment_at = models.DateTimeField(verbose_name="입관 일정")
    departure_at = models.DateTimeField(verbose_name="발인 일정")
    comment_count = models.PositiveBigIntegerField(verbose_name="댓글수", default=0, editable=False)

    class Meta:
        db_table = "passing_notice"
        verbose_name = "선종 안내"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
