from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from app.email_verifier.models import EmailVerifier
from app.email_verifier.v1.permissions import EmailVerifierPermission
from app.email_verifier.v1.serializers import EmailVerifierConfirmSerializer, EmailVerifierCreateSerializer


@extend_schema_view(
    create=extend_schema(summary="이메일 검증 등록"),
    confirm=extend_schema(summary="이메일 검증 확인"),
)
class EmailVerifierViewSet(
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = EmailVerifier.objects.all()
    serializer_class = EmailVerifierCreateSerializer
    permission_classes = [EmailVerifierPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(methods=["post"], detail=False, serializer_class=EmailVerifierConfirmSerializer)
    def confirm(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
