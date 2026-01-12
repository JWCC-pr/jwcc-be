from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app.room_reservation.v1.views import RepeatRoomReservationViewSet, RoomReservationViewSet

router = DefaultRouter()
router.register("room_reservation", RoomReservationViewSet, basename="room_reservation")
router.register("repeat_room_reservation", RepeatRoomReservationViewSet, basename="repeat_room_reservation")

urlpatterns = [
    path("", include(router.urls)),
]
