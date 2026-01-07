from rest_framework import serializers

from app.room_reservation.models import RoomReservation


class RoomReservationSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source="room.name", read_only=True)

    class Meta:
        model = RoomReservation
        fields = [
            "id",
            "room",
            "room_name",
            "date",
            "start_at",
            "end_at",
            "created_at",
            "updated_at",
        ]
