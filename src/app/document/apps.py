from django.apps import AppConfig


class DocumentConfig(AppConfig):
    name = "app.document"
    verbose_name = "15.자료"

    def ready(self):
        import app.document.signals
