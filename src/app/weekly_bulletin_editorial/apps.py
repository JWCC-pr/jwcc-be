from django.apps import AppConfig


class WeeklyBulletinEditorialConfig(AppConfig):
    name = "app.weekly_bulletin_editorial"
    verbose_name = "22.주보7면"

    def ready(self):
        import app.weekly_bulletin_editorial.signals
