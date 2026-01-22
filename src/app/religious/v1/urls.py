from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.religious.v1.views import ReligiousViewSet

router = DefaultRouter()
router.register("religious", ReligiousViewSet, basename="religious")

urlpatterns = [
    path("", include(router.urls)),
]
