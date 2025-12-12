from django.apps import AppConfig


class BoardCommentConfig(AppConfig):
    name = "app.board_comment"

    def ready(self):
        import app.board_comment.signals
