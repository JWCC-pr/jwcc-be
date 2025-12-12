from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.pastoral_guidelines.v1.views import PastoralGuidelinesViewSet

router = DefaultRouter()
router.register("pastoral_guidelines", PastoralGuidelinesViewSet, basename="pastoral_guidelines")

urlpatterns = [
    path("", include(router.urls)),
]
