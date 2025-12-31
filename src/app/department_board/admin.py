from django.contrib import admin

from app.department_board.models import DepartmentBoard


@admin.register(DepartmentBoard)
class DepartmentBoardAdmin(admin.ModelAdmin):
    pass
