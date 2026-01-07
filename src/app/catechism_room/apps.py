from django.apps import AppConfig


class CatechismRoomConfig(AppConfig):
    name = "app.catechism_room"

    def ready(self):
        import app.catechism_room.signals
