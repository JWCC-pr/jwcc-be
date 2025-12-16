from django.apps import AppConfig


class SubDepartmentConfig(AppConfig):
    name = "app.sub_department"

    def ready(self):
        import app.sub_department.signals
