from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.email_verifier.v1.views import EmailVerifierViewSet

router = DefaultRouter()
router.register("email_verifier", EmailVerifierViewSet, basename="email_verifier")

urlpatterns = [
    path("", include(router.urls)),
]
