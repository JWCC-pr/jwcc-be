from django.apps import AppConfig


class LiturgyFlowerLikeConfig(AppConfig):
    name = "app.liturgy_flower_like"

    def ready(self):
        import app.liturgy_flower_like.signals
