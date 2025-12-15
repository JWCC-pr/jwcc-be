from django.apps import AppConfig


class WeeklyBulletinHitConfig(AppConfig):
    name = "app.weekly_bulletin_hit"

    def ready(self):
        import app.weekly_bulletin_hit.signals
