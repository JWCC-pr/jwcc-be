from django.apps import AppConfig


class BoardImageConfig(AppConfig):
    name = "app.board_image"

    def ready(self):
        import app.board_image.signals
