from django.contrib import admin

from app.department.models import Department
from app.sub_department.models import SubDepartment


class SubDepartmentInline(admin.TabularInline):
    model = SubDepartment
    extra = 0


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [SubDepartmentInline]
    list_display = ["name"]
    search_fields = ["name"]
    search_help_text = "분과명으로 검색하세요."
