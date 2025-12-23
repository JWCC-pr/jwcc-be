from django.apps import AppConfig


class PriestConfig(AppConfig):
    name = "app.priest"
    verbose_name = "17.사제관리"

    def ready(self):
        import app.priest.signals
