from django.contrib import admin

from app.room_reservation.models import RoomReservation


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "date", "start_at", "end_at", "created_at"]
    list_filter = ["room", "date"]
    search_fields = ["room__name"]
    search_help_text = "교리실명으로 검색하세요."
