from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.document_file.v1.views import DocumentFileViewSet

router = DefaultRouter()
router.register("document_file", DocumentFileViewSet, basename="document_file")

urlpatterns = [
    path("", include(router.urls)),
]
