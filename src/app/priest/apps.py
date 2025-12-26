from django.apps import AppConfig


class PriestConfig(AppConfig):
    name = "app.priest"
    verbose_name = "15.본당 사제"

    def ready(self):
        import app.priest.signals
