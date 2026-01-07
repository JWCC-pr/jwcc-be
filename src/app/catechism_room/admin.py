from django.contrib import admin

from app.catechism_room.models import CatechismRoom


@admin.register(CatechismRoom)
class CatechismRoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "location", "created_at"]
    search_fields = ["name", "location"]
    search_help_text = "교리실명, 위치로 검색하세요."
