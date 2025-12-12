from django.contrib import admin

from app.department.models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    search_help_text = "분과명으로 검색하세요."
