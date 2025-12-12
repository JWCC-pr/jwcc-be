from django.db import models

from app.common.models import BaseModel


class EmailVerifier(BaseModel):
    email = models.EmailField(verbose_name="이메일")
    code = models.CharField(verbose_name="인증번호", max_length=6)
    token = models.CharField(verbose_name="토큰", max_length=40)

    class Meta:
        db_table = "email_verifier"
        verbose_name = "이메일 검증"
        verbose_name_plural = verbose_name
        ordering = ["-created_at"]
