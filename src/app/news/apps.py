from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = "app.news"
    verbose_name = "14.본당소식"

    def ready(self):
        import app.news.signals
