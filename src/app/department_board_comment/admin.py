from django.contrib import admin

from app.department_board_comment.models import DepartmentBoardComment


@admin.register(DepartmentBoardComment)
class DepartmentBoardCommentAdmin(admin.ModelAdmin):
    pass
