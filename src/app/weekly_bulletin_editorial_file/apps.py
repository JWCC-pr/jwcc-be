from django.apps import AppConfig


class WeeklyBulletinEditorialFileConfig(AppConfig):
    name = "app.weekly_bulletin_editorial_file"

    def ready(self):
        import app.weekly_bulletin_editorial_file.signals
