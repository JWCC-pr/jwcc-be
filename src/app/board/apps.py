from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = "app.board"

    def ready(self):
        import app.board.signals
