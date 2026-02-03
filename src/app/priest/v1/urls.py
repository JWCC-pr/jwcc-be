from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.priest.v1.views import PriestViewSet

router = DefaultRouter()
router.register("priest", PriestViewSet, basename="priest")

urlpatterns = [
    path("", include(router.urls)),
]
