from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.notice_file.v1.views import NoticeFileViewSet

router = DefaultRouter()
router.register("notice_file", NoticeFileViewSet, basename="notice_file")

urlpatterns = [
    path("", include(router.urls)),
]
