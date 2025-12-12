from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from app.department.models import Department


@admin.register(Department)
class DepartmentAdmin(OrderedModelAdmin):
    list_display = ["move_up_down_links", "name"]
    search_fields = ["name"]
    search_help_text = "분과명으로 검색하세요."
