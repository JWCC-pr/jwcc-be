from django.apps import AppConfig


class PriestHistoryConfig(AppConfig):
    name = "app.priest_history"
    verbose_name = "17.본당 출신 사제"

    def ready(self):
        import app.priest_history.signals
