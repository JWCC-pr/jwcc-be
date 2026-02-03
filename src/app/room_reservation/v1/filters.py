import django_filters

from app.room_reservation.models import CatechismRoom, RoomReservation


class RoomReservationFilter(django_filters.FilterSet):
    room = django_filters.NumberFilter(field_name="room_id", label="교리실 ID")
    date = django_filters.DateFilter(field_name="date", label="예약 날짜")

    class Meta:
        model = RoomReservation
        fields = ["room", "date"]


class CatechismRoomFilter(django_filters.FilterSet):
    class Meta:
        model = CatechismRoom
        fields = []
