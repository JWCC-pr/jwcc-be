from django.apps import AppConfig


class DepartmentBoardConfig(AppConfig):
    name = "app.department_board"

    def ready(self):
        import app.department_board.signals
