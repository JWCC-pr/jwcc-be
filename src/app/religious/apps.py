from django.apps import AppConfig


class ReligiousConfig(AppConfig):
    name = "app.religious"
    verbose_name = "16.본당수도자관리"

    def ready(self):
        import app.religious.signals
