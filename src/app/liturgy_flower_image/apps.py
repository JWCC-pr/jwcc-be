from django.apps import AppConfig


class LiturgyFlowerImageConfig(AppConfig):
    name = "app.liturgy_flower_image"

    def ready(self):
        import app.liturgy_flower_image.signals
