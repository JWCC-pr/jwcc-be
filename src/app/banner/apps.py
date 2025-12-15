from django.apps import AppConfig


class BannerConfig(AppConfig):
    name = "app.banner"
    verbose_name = "05.배너"

    def ready(self):
        import app.banner.signals
