from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.passing_notice_comment.v1.views import PassingNoticeCommentViewSet

router = DefaultRouter()
router.register("comment", PassingNoticeCommentViewSet, basename="passing_notice_comment")

urlpatterns = [
    path("passing_notice/<int:passing_notice_id>/", include(router.urls)),
]
