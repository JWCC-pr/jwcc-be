from django.apps import AppConfig


class EmailVerifierConfig(AppConfig):
    name = "app.email_verifier"

    def ready(self):
        import app.email_verifier.signals
