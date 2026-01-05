from django.apps import AppConfig


class DepartmentBoardConfig(AppConfig):
    name = "app.department_board"
    verbose_name = "21.분과게시글"

    def ready(self):
        import app.department_board.signals
