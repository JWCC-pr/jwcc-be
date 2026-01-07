from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin, OrderedTabularInline, OrderedInlineModelAdminMixin

from app.department.models import Department
from app.sub_department.models import SubDepartment


class SubDepartmentInline(OrderedTabularInline):
    model = SubDepartment
    fields = ("id", "name", "order", "move_up_down_links")
    readonly_fields = ("order", "move_up_down_links")
    extra = 0


@admin.register(Department)
class DepartmentAdmin(OrderedInlineModelAdminMixin, OrderedModelAdmin):
    inlines = [SubDepartmentInline]
    list_display = ["id", "name", "order", "move_up_down_links"]
    search_fields = ["name"]
    search_help_text = "분과명으로 검색하세요."
