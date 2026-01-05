from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_editorial.v1.views import (
    MyeongdoViewSet,
    DraftViewSet,
    FinalViewSet,
    TemplateViewSet,
)

router = DefaultRouter()
router.register("editorials/myeongdo", MyeongdoViewSet, basename="editorials-myeongdo")
router.register("editorials/draft", DraftViewSet, basename="editorials-draft")
router.register("editorials/final", FinalViewSet, basename="editorials-final")
router.register("editorials/template", TemplateViewSet, basename="editorials-template")

urlpatterns = [
    path("", include(router.urls)),
]
