from django.apps import AppConfig


class WeeklyBulletinRequestConfig(AppConfig):
    name = "app.weekly_bulletin_request"

    def ready(self):
        import app.weekly_bulletin_request.signals
