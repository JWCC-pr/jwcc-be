from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app.room_reservation.v1.views import RoomReservationViewSet

router = DefaultRouter()
router.register("room_reservation", RoomReservationViewSet, basename="room_reservation")

urlpatterns = [
    path("", include(router.urls)),
]
