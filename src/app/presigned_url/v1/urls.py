from django.urls import path

from app.presigned_url.v1.views import PresignedDownloadUrlCreateView, PresignedUrlCreateView

urlpatterns = [
    path("presigned_url/", PresignedUrlCreateView.as_view()),
    path("presigned_url/download/", PresignedDownloadUrlCreateView.as_view()),
]
