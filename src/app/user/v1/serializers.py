from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError as DjangoValidationError
from django.template import loader
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from app.email_log.models import EmailLog
from app.email_verifier.models import EmailVerifier
from app.user.models import User
from app.user.validators import validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "baptismal_name",
            "postcode",
            "base_address",
            "detail_address",
            "birth",
        ]


class UserLoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(label="액세스토큰", read_only=True)
    refresh_token = serializers.CharField(label="리프레시토큰", read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "access_token",
            "refresh_token",
        ]
        extra_kwargs = {
            "email": {"write_only": True, "validators": []},
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        try:
            attrs["user"] = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise ValidationError(["인증정보가 일치하지 않습니다."])
        if not attrs["user"].check_password(attrs["password"]):
            raise ValidationError(["인증정보가 일치하지 않습니다."])
        if not attrs["user"].is_active:
            raise ValidationError(["가입승인이 되지 않았습니다."])
        return attrs

    def create(self, validated_data):
        validated_data["user"].last_login = timezone.localtime()
        validated_data["user"].save()
        return validated_data["user"]


class UserRegisterSerializer(serializers.ModelSerializer):
    sub_department_ids = serializers.ListSerializer(label="분과 ID", write_only=True, child=serializers.IntegerField())
    email_verifier_token = serializers.CharField(label="이메일 검증 토큰", write_only=True)
    access_token = serializers.CharField(label="액세스토큰", read_only=True)
    refresh_token = serializers.CharField(label="리프레시토큰", read_only=True)

    class Meta:
        model = User
        fields = [
            "sub_department_ids",
            "email",
            "email_verifier_token",
            "password",
            "name",
            "baptismal_name",
            "postcode",
            "base_address",
            "detail_address",
            "birth",
            "access_token",
            "refresh_token",
        ]

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise ValidationError({"email": ["이미 사용중인 이메일입니다."]})
        if not EmailVerifier.objects.filter(email=attrs["email"], token=attrs.pop("email_verifier_token")).exists():
            raise ValidationError({"email_verifier_token": ["이메일 검증에 실패했습니다."]})
        return attrs

    def create(self, validated_data):
        sub_department_ids = validated_data.pop("sub_department_ids")
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        user.sub_department_set.set(sub_department_ids)

        return user


class UserRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh_token"])

        data = {"access_token": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh_token"] = str(refresh)

        return data


class UserPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        try:
            user = User.objects.get(**validated_data)
            self._send_password_reset_email(user)
        except User.DoesNotExist:
            pass

        return validated_data

    def _send_password_reset_email(self, user):
        request = self.context["request"]

        subject = "잠원동 성당 비밀번호 초기화 인증 메일"
        context = {
            "domain": settings.DOMAIN,
            "site_name": settings.SITE_NAME,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            "token": default_token_generator.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        }
        content = loader.render_to_string("password_reset.html", context)
        email_log = EmailLog.objects.create(
            email=user.email,
            title=subject,
            content=content,
        )
        email_log.send()


class UserPasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(attrs["uid"])))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = AnonymousUser()
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]
        token = attrs["token"]

        if not user.is_authenticated:
            raise ValidationError("존재하지 않는 유저입니다.")

        if not default_token_generator.check_token(user, token):
            raise ValidationError("이미 비밀번호를 변경하셨습니다.")

        errors = dict()
        if password != password_confirm:
            errors["password"] = ["비밀번호가 일치하지 않습니다."]
            errors["password_confirm"] = ["비밀번호가 일치하지 않습니다."]
        else:
            try:
                validate_password(password)
            except DjangoValidationError as error:
                errors["password"] = list(error)
                errors["password_confirm"] = list(error)
        if errors:
            raise ValidationError(errors)

        return attrs

    def update(self, instance, validated_data):
        password = validated_data["password"]
        instance.set_password(password)
        instance.save()

        return instance
