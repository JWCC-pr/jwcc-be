from django.contrib import admin

from app.priest.models import Associate, Pastor, Priest


@admin.register(Priest)
class PriestAdmin(admin.ModelAdmin):
    list_display = ["name", "baptismal_name", "is_retired"]


@admin.register(Pastor)
class PastorAdmin(admin.ModelAdmin):
    list_display = ["name", "baptismal_name", "division", "start_date", "end_date", "is_retired"]


@admin.register(Associate)
class AssociateAdmin(admin.ModelAdmin):
    list_display = ["name", "baptismal_name", "assistant_system", "start_date", "end_date", "is_retired"]
