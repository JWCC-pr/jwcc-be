from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from app.user.models import User
from app.user.v1.serializers import (
    UserLoginSerializer,
    UserPasswordResetConfirmSerializer,
    UserPasswordResetSerializer,
    UserRefreshSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


@extend_schema_view(
    retrieve=extend_schema(summary="유저 조회"),
    destroy=extend_schema(summary="유저 삭제(탈퇴)"),
    login=extend_schema(summary="유저 로그인"),
    refresh=extend_schema(summary="유저 리프레시"),
    register=extend_schema(summary="유저 회원가입"),
    password_reset=extend_schema(summary="유저 비밀번호 초기화 메일 발송"),
    password_reset_confirm=extend_schema(summary="유저 비밀번호 재설정"),
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_value_regex = "me"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("sub_department_set")
        return queryset

    def get_object(self):
        if self.kwargs.get("pk") == "me":
            return self.queryset.get(id=self.request.user.id)
        return super().get_object()

    def _create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, serializer_class=UserLoginSerializer, permission_classes=[])
    def login(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False, serializer_class=UserRefreshSerializer, permission_classes=[])
    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, serializer_class=UserRegisterSerializer, permission_classes=[])
    def register(self, request, *args, **kwargs):
        return self._create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False, serializer_class=UserPasswordResetSerializer, permission_classes=[])
    def password_reset(self, request, *args, **kwargs):
        """
        이메일을 통해 비밀번호 재설정 가능한 link을 발급받습니다.
        """
        return self._create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False, serializer_class=UserPasswordResetConfirmSerializer, permission_classes=[])
    def password_reset_confirm(self, request, *args, **kwargs):
        """
        유저 비밀번호 초기화 메일 발송 API를 통해 발급 받은 link를 통해 비밀번호를 재설정합니다.
        """
        return self._create(request, *args, **kwargs)
