import hashlib
import random

from django.template import loader
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.email_log.models import EmailLog
from app.email_verifier.models import EmailVerifier
from app.user.models import User


class EmailVerifierCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerifier
        fields = ["id", "email"]

    def validate(self, attrs):
        email = attrs["email"]

        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": ["이미 가입된 이메일입니다."]})

        code = "".join([str(random.randint(0, 9)) for i in range(6)])
        created = timezone.localtime()
        hash_string = str(email) + code + str(created.timestamp())
        token = hashlib.sha1(hash_string.encode("utf-8")).hexdigest()

        attrs.update(
            {
                "code": code,
                "token": token,
            }
        )

        try:
            self._send_code(attrs)
        except Exception:
            raise ValidationError("인증번호 전송 실패")

        return attrs

    def _send_code(self, attrs):
        subject = "잠원동 성당 회원가입 인증메일"
        context = {
            "subject": subject,
            "message": f'잠원동 성당 회원가입 인증코드 [{attrs["code"]}]',
        }
        content = loader.render_to_string("email_verification.html", context)
        email_log = EmailLog.objects.create(
            email=attrs["email"],
            title=subject,
            content=content,
        )
        email_log.send()


class EmailVerifierConfirmSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)

    class Meta:
        model = EmailVerifier
        fields = ["email", "code", "token"]
        extra_kwargs = {
            "token": {"read_only": True},
        }

    def validate(self, attrs):
        email = attrs["email"]
        code = attrs["code"]
        try:
            email_verifier = EmailVerifier.objects.get(email=email, code=code)
        except EmailVerifier.DoesNotExist:
            raise ValidationError({"code": ["인증번호가 일치하지 않습니다."]})

        attrs.update({"token": email_verifier.token})
        return attrs

    def create(self, validated_data):
        return validated_data
