from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.document.v1.views import DocumentViewSet

router = DefaultRouter()
router.register("document", DocumentViewSet, basename="document")

urlpatterns = [
    path("", include(router.urls)),
]
