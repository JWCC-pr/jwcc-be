from django.contrib import admin
from django.core.exceptions import ValidationError

from app.room_reservation.models import RepeatRoomReservation, RoomReservation
from app.room_reservation.v1.serializers import RepeatRoomReservationSerializer


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ["id", "room", "title", "date", "start_at", "end_at", "repeat", "created_at"]
    list_filter = ["room", "date", "repeat"]
    search_fields = ["room__name", "title"]
    search_help_text = "교리실명, 예약 제목으로 검색하세요."


@admin.register(RepeatRoomReservation)
class RepeatRoomReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "title",
        "repeat_type",
        "start_date",
        "end_date",
        "start_at",
        "end_at",
        "reservation_count",
        "created_at",
    ]
    list_filter = ["room", "repeat_type"]
    search_fields = ["room__name", "title"]
    search_help_text = "교리실명, 예약 제목으로 검색하세요."

    @admin.display(description="예약 수")
    def reservation_count(self, obj):
        return obj.reservation_set.count()

    def save_model(self, request, obj, form, change):
        if change:
            obj.reservation_set.all().delete()

        serializer = RepeatRoomReservationSerializer(data=form.cleaned_data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise ValidationError(str(e))
