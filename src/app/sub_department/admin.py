from django.contrib import admin

from app.sub_department.models import SubDepartment


@admin.register(SubDepartment)
class SubDepartmentAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    raw_id_fields = ["department"]
