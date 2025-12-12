from django.apps import AppConfig


class BoardHitConfig(AppConfig):
    name = "app.board_hit"

    def ready(self):
        import app.board_hit.signals
