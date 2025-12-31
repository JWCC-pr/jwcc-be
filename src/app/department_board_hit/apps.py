from django.apps import AppConfig


class DepartmentBoardHitConfig(AppConfig):
    name = "app.department_board_hit"

    def ready(self):
        import app.department_board_hit.signals
