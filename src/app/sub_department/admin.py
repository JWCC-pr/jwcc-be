# from django.contrib import admin
# from ordered_model.admin import OrderedModelAdmin
#
# from app.sub_department.models import SubDepartment
#
#
# @admin.register(SubDepartment)
# class SubDepartmentAdmin(OrderedModelAdmin):
#     list_display = ("id", "name", "department", "move_up_down_links")
#     list_filter = ("department",)  # 실무에서 매우 유용
#     raw_id_fields = ("department",)
#     ordering = ("department", "order")
