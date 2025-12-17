from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = "app.news"

    def ready(self):
        import app.news.signals
