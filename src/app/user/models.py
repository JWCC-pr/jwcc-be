from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from app.common.models import BaseModel, BaseModelMixin


class UserGradeChoices(models.IntegerChoices):
    GRADE_01 = 1, "총관리자"
    GRADE_02 = 2, "사제 및 수도자"
    GRADE_03 = 3, "사무실"
    GRADE_04 = 4, "단체장"
    GRADE_05 = 5, "명도회"
    GRADE_06 = 6, "본당 신자"
    GRADE_07 = 7, "타본당 신자"


class User(BaseModelMixin, AbstractBaseUser):
    sub_department_set = models.ManyToManyField("department.SubDepartment", verbose_name="세부분과", blank=True)
    email = models.EmailField(verbose_name="유저네임", unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    postcode = models.CharField(verbose_name="우편번호", max_length=6)
    base_address = models.CharField(verbose_name="기본주소", max_length=200)
    detail_address = models.CharField(verbose_name="상세주소", max_length=200)
    birth = models.DateField(verbose_name="생년월일")
    grade = models.PositiveIntegerField(
        verbose_name="등급", choices=UserGradeChoices, default=UserGradeChoices.GRADE_07
    )

    is_authenticated = True
    is_active = models.BooleanField(verbose_name="가입승인 여부", default=False, editable=False)

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    @property
    def access_token(self):
        return AccessToken.for_user(self)

    @property
    def refresh_token(self):
        return RefreshToken.for_user(self)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)
