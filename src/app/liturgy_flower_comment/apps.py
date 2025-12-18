from django.apps import AppConfig


class LiturgyFlowerCommentConfig(AppConfig):
    name = "app.liturgy_flower_comment"

    def ready(self):
        import app.liturgy_flower_comment.signals
