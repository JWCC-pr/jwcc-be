from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = "app.schedule"
    verbose_name = "07.일정"

    def ready(self):
        import app.schedule.signals
