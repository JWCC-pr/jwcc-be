from django.apps import AppConfig


class ReligiousConfig(AppConfig):
    name = "app.religious"
    verbose_name = "16.본당 수도자"

    def ready(self):
        import app.religious.signals
