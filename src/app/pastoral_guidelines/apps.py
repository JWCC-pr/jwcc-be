from django.apps import AppConfig


class PastoralGuidelinesConfig(AppConfig):
    name = "app.pastoral_guidelines"
    verbose_name = "05.사목지침"

    def ready(self):
        import app.pastoral_guidelines.signals
