from django.apps import AppConfig


class LiturgyFlowerHitConfig(AppConfig):
    name = "app.liturgy_flower_hit"

    def ready(self):
        import app.liturgy_flower_hit.signals
