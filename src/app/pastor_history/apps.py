from django.apps import AppConfig


class PastorHistoryConfig(AppConfig):
    name = "app.pastor_history"
    verbose_name = "19.역대 주임신부"

    def ready(self):
        import app.pastor_history.signals
