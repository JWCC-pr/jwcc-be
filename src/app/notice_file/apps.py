from django.apps import AppConfig


class NoticeFileConfig(AppConfig):
    name = "app.notice_file"

    def ready(self):
        import app.notice_file.signals
