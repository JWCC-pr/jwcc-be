from django.apps import AppConfig


class PassingNoticeConfig(AppConfig):
    name = "app.passing_notice"
    verbose_name = "07.선종 안내"

    def ready(self):
        import app.passing_notice.signals
