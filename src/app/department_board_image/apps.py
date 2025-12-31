from django.apps import AppConfig


class DepartmentBoardImageConfig(AppConfig):
    name = "app.department_board_image"

    def ready(self):
        import app.department_board_image.signals
