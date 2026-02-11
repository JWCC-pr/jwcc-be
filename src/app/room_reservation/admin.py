from django.contrib import admin
from django.core.exceptions import ValidationError

from app.room_reservation.models import CatechismRoom, RepeatRoomReservation, RoomReservation
from app.room_reservation.v1.serializers import RepeatRoomReservationSerializer


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "title",
        "user_name",
        "organization_name",
        "date",
        "start_at",
        "end_at",
        "repeat",
        "created_by",
    ]
    list_filter = ["room", "date", "repeat"]
    search_fields = ["room__name", "title", "user_name", "organization_name"]
    search_help_text = "교리실명, 예약 제목, 사용단체명으로 검색하세요."


@admin.register(RepeatRoomReservation)
class RepeatRoomReservationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "room",
        "title",
        "user_name",
        "organization_name",
        "repeat_type",
        "start_date",
        "end_date",
        "start_at",
        "end_at",
        "reservation_count",
        "created_by",
        "created_at",
    ]
    list_filter = ["room", "repeat_type"]
    search_fields = ["room__name", "title", "user_name", "organization_name"]
    search_help_text = "교리실명, 예약 제목, 사용단체명으로 검색하세요."

    @admin.display(description="예약 수")
    def reservation_count(self, obj):
        return obj.reservation_set.count()

    def save_model(self, request, obj, form, change):
        if change:
            obj.reservation_set.all().delete()

        # Admin form에서는 ForeignKey가 객체로 전달되므로 pk로 변환
        data = form.cleaned_data.copy()
        data["room"] = data["room"].pk

        serializer = RepeatRoomReservationSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            raise ValidationError(str(e))


@admin.register(CatechismRoom)
class CatechismRoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "location", "created_at"]
    search_fields = ["name", "location"]
    search_help_text = "교리실명, 위치로 검색하세요."
