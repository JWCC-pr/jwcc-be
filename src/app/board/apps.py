from django.apps import AppConfig


class BoardConfig(AppConfig):
    name = "app.board"
    verbose_name = "14.자유게시글"

    def ready(self):
        import app.board.signals
