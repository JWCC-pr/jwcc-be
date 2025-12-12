from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.passing_notice.v1.views import PassingNoticeViewSet

router = DefaultRouter()
router.register("passing_notice", PassingNoticeViewSet, basename="passing_notice")

urlpatterns = [
    path("", include(router.urls)),
]
