from django.apps import AppConfig


class PassingNoticeCommentConfig(AppConfig):
    name = "app.passing_notice_comment"

    def ready(self):
        import app.passing_notice_comment.signals
