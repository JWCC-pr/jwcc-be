import requests
from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from app.common.models import BaseModel


class EmailLogStatus(models.TextChoices):
    READY = "R", "대기"
    SUCCESS = "S", "성공"
    FAILURE = "F", "실패"


class EmailLog(BaseModel):
    email = models.EmailField(verbose_name="수신자")
    title = models.CharField(verbose_name="제목", max_length=128)
    content = models.TextField(verbose_name="내용")
    status = models.CharField(verbose_name="상태", max_length=1, choices=EmailLogStatus, default=EmailLogStatus.READY)
    fail_reason = models.TextField(verbose_name="실패사유", blank=True, default="")

    class Meta:
        db_table = "email_log"
        verbose_name = "이메일 로그"
        verbose_name_plural = verbose_name

    def send(self):
        response = requests.post(
            "https://api.mailgun.net/v3/jwcc.or.kr/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": self.email,
                "subject": self.title,
                "html": self.content,
            },
        )
        print(response.text)
        return response
        return requests.post(
            "https://api.mailgun.net/v3/jwcc.or.kr/messages",
            auth=("api", settings.MAILGUN_API_KEY),
            data={
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": self.email,
                "subject": self.title,
                "html": self.content,
            },
        )
