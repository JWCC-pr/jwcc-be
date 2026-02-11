from rest_framework.exceptions import ValidationError

from app.room_reservation.models import RoomReservation


def find_conflicts(*, room, start_at, end_at, dates, exclude_pk=None):
    qs = RoomReservation.objects.filter(
        room=room,
        date__in=dates,
        start_at__lt=end_at,
        end_at__gt=start_at,
    ).select_related("room")

    if exclude_pk:
        qs = qs.exclude(pk=exclude_pk)

    conflicts = [
        {
            "room_id": reservation.room_id,
            "room_name": reservation.room.name,
            "date": reservation.date,
            "start_at": reservation.start_at,
            "end_at": reservation.end_at,
        }
        for reservation in qs
    ]
    conflicts.sort(key=lambda item: (item["date"], item["start_at"], item["end_at"]))

    if conflicts:
        raise ValidationError(
            {
                "detail": "반복 설정한 예약 일정과 기존 예약이 겹쳐 예약이 불가능합니다.",
                "conflicts": conflicts,
            }
        )
