from django.apps import AppConfig


class ContactConfig(AppConfig):
    name = "app.contact"
    verbose_name = "04.연락처"

    def ready(self):
        import app.contact.signals
