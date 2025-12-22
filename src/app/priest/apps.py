from django.apps import AppConfig


class PriestConfig(AppConfig):
    name = "app.priest"

    def ready(self):
        import app.priest.signals
