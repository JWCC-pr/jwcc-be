from django.apps import AppConfig


class NoticeConfig(AppConfig):
    name = "app.notice"
    verbose_name = "04.공지사항"

    def ready(self):
        import app.notice.signals
