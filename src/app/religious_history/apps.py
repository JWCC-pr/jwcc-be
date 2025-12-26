from django.apps import AppConfig


class ReligiousHistoryConfig(AppConfig):
    name = "app.religious_history"
    verbose_name = "18.본당 출신 수도자"

    def ready(self):
        import app.religious_history.signals
