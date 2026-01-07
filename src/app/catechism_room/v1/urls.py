from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.catechism_room.v1.views import CatechismRoomViewSet

router = DefaultRouter()
router.register("catechism_room", CatechismRoomViewSet, basename="catechism_room")

urlpatterns = [
    path("", include(router.urls)),
]
