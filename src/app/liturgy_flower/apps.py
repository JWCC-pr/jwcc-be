from django.apps import AppConfig


class LiturgyFlowerConfig(AppConfig):
    name = "app.liturgy_flower"
    verbose_name = "11.전례꽃"

    def ready(self):
        import app.liturgy_flower.signals
