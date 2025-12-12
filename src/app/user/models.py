from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from app.common.models import BaseModel


class User(BaseModel):
    department = models.ForeignKey("department.Department", verbose_name="분과", on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="유저네임", unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    name = models.CharField(verbose_name="이름", max_length=20)
    baptismal_name = models.CharField(verbose_name="세례명", max_length=40)
    postcode = models.CharField(verbose_name="우편번호", max_length=6)
    base_address = models.CharField(verbose_name="기본주소", max_length=200)
    detail_address = models.CharField(verbose_name="상세주소", max_length=200)
    birth = models.DateField(verbose_name="생년월일")
    is_accepted = models.BooleanField(verbose_name="가입승인 여부", default=False)

    is_authenticated = True
    is_active = True

    class Meta:
        db_table = "user"
        verbose_name = "유저"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.email

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
