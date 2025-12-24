from django.apps import AppConfig


class DepartmentConfig(AppConfig):
    name = "app.department"
    verbose_name = "03.분과"

    def ready(self):
        import app.department.signals
