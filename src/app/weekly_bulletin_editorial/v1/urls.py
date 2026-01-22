from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.weekly_bulletin_editorial.v1.views import DraftViewSet, FinalViewSet, MyeongdoViewSet, TemplateViewSet

router = DefaultRouter()
router.register("editorials/myeongdo", MyeongdoViewSet, basename="editorials-myeongdo")
router.register("editorials/draft", DraftViewSet, basename="editorials-draft")
router.register("editorials/final", FinalViewSet, basename="editorials-final")
router.register("editorials/template", TemplateViewSet, basename="editorials-template")

urlpatterns = [
    path("", include(router.urls)),
]
