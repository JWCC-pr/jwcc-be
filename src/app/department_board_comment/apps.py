from django.apps import AppConfig


class DepartmentBoardCommentConfig(AppConfig):
    name = "app.department_board_comment"

    def ready(self):
        import app.department_board_comment.signals
