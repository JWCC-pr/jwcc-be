from django.apps import AppConfig


class BoardLikeConfig(AppConfig):
    name = "app.board_like"

    def ready(self):
        import app.board_like.signals
