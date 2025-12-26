from django.apps import AppConfig


class AssistantPriestHistoryConfig(AppConfig):
    name = "app.assistant_priest_history"
    verbose_name = "20.역대 부주임/보좌신부"

    def ready(self):
        import app.assistant_priest_history.signals
