from django.apps import AppConfig


class WeeklyBulletinConfig(AppConfig):
    name = "app.weekly_bulletin"
    verbose_name = "09.주보"

    def ready(self):
        import app.weekly_bulletin.signals
