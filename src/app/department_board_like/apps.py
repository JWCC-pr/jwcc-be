from django.apps import AppConfig


class DepartmentBoardLikeConfig(AppConfig):
    name = "app.department_board_like"

    def ready(self):
        import app.department_board_like.signals
