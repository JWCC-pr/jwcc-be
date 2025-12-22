from django.apps import AppConfig


class ReligiousConfig(AppConfig):
    name = "app.religious"

    def ready(self):
        import app.religious.signals
