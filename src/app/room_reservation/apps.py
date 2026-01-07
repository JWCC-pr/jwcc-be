from django.apps import AppConfig


class RoomReservationConfig(AppConfig):
    name = "app.room_reservation"

    def ready(self):
        import app.room_reservation.signals
