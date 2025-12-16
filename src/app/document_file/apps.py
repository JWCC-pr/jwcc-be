from django.apps import AppConfig


class DocumentFileConfig(AppConfig):
    name = "app.document_file"

    def ready(self):
        import app.document_file.signals
