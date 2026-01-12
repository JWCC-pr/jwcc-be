from rest_framework.exceptions import ValidationError

from app.room_reservation.models import RoomReservation


def validate_no_overlap(*, room, start_at, end_at, dates, exclude_pk=None):
    conflicts = [
        date
        for date in dates
        if RoomReservation.objects.has_overlap(
            room=room,
            date=date,
            start_at=start_at,
            end_at=end_at,
            exclude_pk=exclude_pk,
        )
    ]

    if conflicts:
        raise ValidationError(f"다음 날짜에 이미 예약이 있습니다: {', '.join(map(str, conflicts))}")
