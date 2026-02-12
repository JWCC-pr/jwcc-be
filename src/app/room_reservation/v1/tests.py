from datetime import date, time

from rest_framework import status
from rest_framework.test import APITestCase

from app.room_reservation.models import CatechismRoom, RepeatRoomReservation, RoomReservation
from app.user.models import User, UserGradeChoices


def create_room():
    return CatechismRoom.objects.create(name="교리실 A")


def create_user(email, grade):
    return User.objects.create(
        email=email,
        password="password",
        name="테스트",
        baptismal_name="테스트",
        postcode="12345",
        base_address="주소",
        detail_address="상세 주소",
        birth=date(2000, 1, 1),
        grade=grade,
    )


class RoomReservationListAPITest(APITestCase):
    MODEL = RoomReservation
    PATH = "/v1/room_reservation/"

    def setUp(self) -> None:
        self.success_user = create_user("success@test.com", UserGradeChoices.GRADE_07)
        self.room = create_room()
        self.MODEL.objects.bulk_create(
            [
                self.MODEL(
                    room=self.room,
                    title=f"예약 {i}",
                    user_name="홍길동",
                    date=date(2026, 1, 1),
                    start_at=time(9, 0),
                    end_at=time(10, 0),
                    created_by=self.success_user,
                )
                for i in range(5)
            ]
        )

    def test_success_response(self):
        self.client.force_authenticate(self.success_user)
        response = self.client.get(self.PATH)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        result_keys = [
            "id",
            "room_id",
            "room_name",
            "repeat",
            "title",
            "user_name",
            "organization_name",
            "date",
            "start_at",
            "end_at",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        for data in response.data["results"]:
            self.assertListEqual(sorted(result_keys), sorted(data.keys()))

    def test_failure_response_authentication_failed(self):
        response = self.client.get(self.PATH)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoomReservationCreateAPITest(APITestCase):
    MODEL = RoomReservation
    PATH = "/v1/room_reservation/"

    def setUp(self) -> None:
        self.success_user = create_user("success@test.com", UserGradeChoices.GRADE_04)
        self.failure_user = create_user("failure@test.com", UserGradeChoices.GRADE_05)
        self.room = create_room()

    def test_success_response(self):
        self.client.force_authenticate(self.success_user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "테스트 예약",
                "user_name": "홍길동",
                "date": "2026-01-02",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertTrue(self.MODEL.objects.filter(id=response.data["id"]).exists())

    def test_failure_response_invalid_failed(self):
        self.client.force_authenticate(self.success_user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "",
                "user_name": "홍길동",
                "date": "2026-01-02",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_failure_response_permission_failed(self):
        self.client.force_authenticate(self.failure_user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "테스트 예약",
                "user_name": "홍길동",
                "date": "2026-01-02",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RoomReservationRetrieveAPITest(APITestCase):
    MODEL = RoomReservation
    PATH = "/v1/room_reservation/{id}/"

    def setUp(self) -> None:
        self.success_user = create_user("success@test.com", UserGradeChoices.GRADE_04)
        self.other_user = create_user("other@test.com", UserGradeChoices.GRADE_07)
        self.room = create_room()
        self.instance = self.MODEL.objects.create(
            room=self.room,
            title="예약",
            user_name="홍길동",
            date=date(2026, 1, 1),
            start_at=time(9, 0),
            end_at=time(10, 0),
            created_by=self.success_user,
        )

    def test_success_response(self):
        self.client.force_authenticate(self.other_user)
        response = self.client.get(self.PATH.format(id=self.instance.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.instance.id)


class RoomReservationUpdateAPITest(APITestCase):
    MODEL = RoomReservation
    PATH = "/v1/room_reservation/{id}/"

    def setUp(self) -> None:
        self.success_user = create_user("success@test.com", UserGradeChoices.GRADE_04)
        self.failure_user = create_user("failure@test.com", UserGradeChoices.GRADE_05)
        self.room = create_room()
        self.instance = self.MODEL.objects.create(
            room=self.room,
            title="예약",
            user_name="홍길동",
            date=date(2026, 1, 1),
            start_at=time(9, 0),
            end_at=time(10, 0),
            created_by=self.success_user,
        )

    def test_success_response(self):
        self.client.force_authenticate(self.success_user)
        response = self.client.put(
            self.PATH.format(id=self.instance.id),
            data={
                "title": "변경 예약",
                "user_name": "이몽룡",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.instance.id)

    def test_failure_response_permission_failed(self):
        self.client.force_authenticate(self.failure_user)
        response = self.client.put(
            self.PATH.format(id=self.instance.id),
            data={
                "title": "변경 예약",
                "user_name": "이몽룡",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RoomReservationDestroyAPITest(APITestCase):
    MODEL = RoomReservation
    PATH = "/v1/room_reservation/{id}/"

    def setUp(self) -> None:
        self.success_user = create_user("success@test.com", UserGradeChoices.GRADE_04)
        self.failure_user = create_user("failure@test.com", UserGradeChoices.GRADE_05)
        self.room = create_room()
        self.instance = self.MODEL.objects.create(
            room=self.room,
            title="예약",
            user_name="홍길동",
            date=date(2026, 1, 1),
            start_at=time(9, 0),
            end_at=time(10, 0),
            created_by=self.success_user,
        )

    def test_success_response(self):
        self.client.force_authenticate(self.success_user)
        response = self.client.delete(self.PATH.format(id=self.instance.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.MODEL.objects.filter(id=self.instance.id).exists())

    def test_failure_response_permission_failed(self):
        self.client.force_authenticate(self.failure_user)
        response = self.client.delete(self.PATH.format(id=self.instance.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RepeatRoomReservationCreateAPITest(APITestCase):
    """반복 예약 생성 API 테스트 — week_of_month 관련 버그 검증 포함."""

    MODEL = RepeatRoomReservation
    PATH = "/v1/repeat_room_reservation/"

    def setUp(self):
        self.user = create_user("admin@test.com", UserGradeChoices.GRADE_01)
        self.room = create_room()

    # ── 요일 반복 + week_of_month ───────────────────────────────

    def test_weekly_week_of_month_1(self):
        """1주차 월요일 반복 → 각 월의 첫 번째 월요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        # 2026-03: 첫 번째 월요일 = 3/2
        # 2026-04: 첫 번째 월요일 = 4/6
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "1주차 월요일 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
                "week_of_month": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertIn(date(2026, 3, 2), reservation_dates)
        self.assertIn(date(2026, 4, 6), reservation_dates)
        self.assertEqual(len(reservation_dates), 2)

    def test_weekly_week_of_month_2(self):
        """2주차 수요일 반복 → 각 월의 두 번째 수요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        # 2026-03: 두 번째 수요일 = 3/11
        # 2026-04: 두 번째 수요일 = 4/8
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "2주차 수요일 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [2],
                "week_of_month": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertIn(date(2026, 3, 11), reservation_dates)
        self.assertIn(date(2026, 4, 8), reservation_dates)
        self.assertEqual(len(reservation_dates), 2)

    def test_weekly_week_of_month_3(self):
        """3주차 금요일 반복 → 각 월의 세 번째 금요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        # 2026-03: 세 번째 금요일 = 3/20
        # 2026-04: 세 번째 금요일 = 4/17
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "3주차 금요일 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [4],
                "week_of_month": 3,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertIn(date(2026, 3, 20), reservation_dates)
        self.assertIn(date(2026, 4, 17), reservation_dates)
        self.assertEqual(len(reservation_dates), 2)

    # ── 요일 반복 (매주, week_of_month 없음) ─────────────────

    def test_weekly_every_week(self):
        """매주 반복(week_of_month=null) → 기간 내 모든 해당 요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "매주 화요일",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-03-31",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [1],
                "week_of_month": None,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        # 2026-03 화요일: 3, 10, 17, 24, 31
        self.assertEqual(reservations.count(), 5)

    # ── 날짜 반복 ─────────────────────────────────────────────

    def test_monthly_date(self):
        """날짜 반복 → 매월 지정 일자가 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "매월 15일",
                "user_name": "홍길동",
                "repeat_type": "monthly_date",
                "start_date": "2026-03-01",
                "end_date": "2026-05-31",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [],
                "month_day": 15,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertEqual(reservation_dates, [date(2026, 3, 15), date(2026, 4, 15), date(2026, 5, 15)])

    # ── week_of_month 추가 케이스 ─────────────────────────────

    def test_weekly_week_of_month_4(self):
        """4주차 토요일 반복 → 각 월의 네 번째 토요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        # 2026-03: 네 번째 토요일 = 3/28
        # 2026-04: 네 번째 토요일 = 4/25
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "4주차 토요일 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [5],
                "week_of_month": 4,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertIn(date(2026, 3, 28), reservation_dates)
        self.assertIn(date(2026, 4, 25), reservation_dates)
        self.assertEqual(len(reservation_dates), 2)

    def test_weekly_week_of_month_multiple_weekdays(self):
        """2주차 월/수 반복 → 각 월의 두 번째 월요일, 두 번째 수요일이 생성되어야 한다."""
        self.client.force_authenticate(self.user)
        # 2026-03: 두 번째 월요일 = 3/9, 두 번째 수요일 = 3/11
        # 2026-04: 두 번째 월요일 = 4/13, 두 번째 수요일 = 4/8
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "2주차 월수 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0, 2],
                "week_of_month": 2,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservations = RoomReservation.objects.filter(repeat_id=response.data["id"])
        reservation_dates = sorted(reservations.values_list("date", flat=True))
        self.assertEqual(len(reservation_dates), 4)
        self.assertIn(date(2026, 3, 9), reservation_dates)
        self.assertIn(date(2026, 3, 11), reservation_dates)
        self.assertIn(date(2026, 4, 13), reservation_dates)
        self.assertIn(date(2026, 4, 8), reservation_dates)

    # ── 권한 ──────────────────────────────────────────────────

    def test_failure_permission_denied(self):
        """GRADE_01 외 유저는 반복 예약 생성 불가."""
        user = create_user("normal@test.com", UserGradeChoices.GRADE_04)
        self.client.force_authenticate(user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "권한 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
                "week_of_month": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ── Validation 에러 ───────────────────────────────────────

    def test_failure_weekly_missing_weekdays(self):
        """요일 반복 시 weekdays 누락 → 400."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "요일 누락",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_start_date_after_end_date(self):
        """시작일 > 종료일 → 400."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "날짜 역전",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-05-01",
                "end_date": "2026-03-01",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_start_at_after_end_at(self):
        """시작 시간 > 종료 시간 → 400."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "시간 역전",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "11:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failure_monthly_date_missing_month_day(self):
        """날짜 반복 시 month_day 누락 → 400."""
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "일자 누락",
                "user_name": "홍길동",
                "repeat_type": "monthly_date",
                "start_date": "2026-03-01",
                "end_date": "2026-05-31",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ── 충돌 ──────────────────────────────────────────────────

    def test_failure_conflict_with_existing_reservation(self):
        """기존 예약과 시간이 겹치면 생성 실패."""
        RoomReservation.objects.create(
            room=self.room,
            title="기존 예약",
            user_name="이몽룡",
            date=date(2026, 3, 2),
            start_at=time(9, 0),
            end_at=time(10, 0),
            created_by=self.user,
        )
        self.client.force_authenticate(self.user)
        response = self.client.post(
            self.PATH,
            data={
                "room_id": self.room.id,
                "title": "충돌 테스트",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
                "week_of_month": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("conflicts", response.data)


class RepeatRoomReservationUpdateAPITest(APITestCase):
    """반복 예약 수정 API 테스트."""

    PATH = "/v1/repeat_room_reservation/{id}/"

    def setUp(self):
        self.user = create_user("admin@test.com", UserGradeChoices.GRADE_01)
        self.room = create_room()
        # 기존 반복 예약 생성
        self.client.force_authenticate(self.user)
        response = self.client.post(
            "/v1/repeat_room_reservation/",
            data={
                "room_id": self.room.id,
                "title": "원본 예약",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
                "week_of_month": 1,
            },
            format="json",
        )
        self.repeat_id = response.data["id"]

    def test_update_recreates_reservations(self):
        """반복 예약 수정 시 개별 예약이 재생성되어야 한다."""
        old_count = RoomReservation.objects.filter(repeat_id=self.repeat_id).count()
        old_ids = set(RoomReservation.objects.filter(repeat_id=self.repeat_id).values_list("id", flat=True))

        response = self.client.put(
            self.PATH.format(id=self.repeat_id),
            data={
                "room_id": self.room.id,
                "title": "수정된 예약",
                "user_name": "이몽룡",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "10:00:00",
                "end_at": "11:00:00",
                "weekdays": [2],
                "week_of_month": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_reservations = RoomReservation.objects.filter(repeat_id=self.repeat_id)
        new_ids = set(new_reservations.values_list("id", flat=True))
        # 기존 예약 ID와 겹치지 않아야 함 (삭제 후 재생성)
        self.assertFalse(old_ids & new_ids)
        # 수정된 제목이 반영되어야 함
        self.assertTrue(all(r.title == "수정된 예약" for r in new_reservations))
        # 수정된 요일(수요일)로 생성
        # 2026-03 첫 번째 수요일 = 3/4, 2026-04 첫 번째 수요일 = 4/1
        reservation_dates = sorted(new_reservations.values_list("date", flat=True))
        self.assertIn(date(2026, 3, 4), reservation_dates)
        self.assertIn(date(2026, 4, 1), reservation_dates)

    def test_update_permission_denied(self):
        """GRADE_01 외 유저는 반복 예약 수정 불가."""
        user = create_user("normal@test.com", UserGradeChoices.GRADE_04)
        self.client.force_authenticate(user)
        response = self.client.put(
            self.PATH.format(id=self.repeat_id),
            data={
                "room_id": self.room.id,
                "title": "수정 시도",
                "user_name": "홍길동",
                "repeat_type": "weekly",
                "start_date": "2026-03-01",
                "end_date": "2026-04-30",
                "start_at": "09:00:00",
                "end_at": "10:00:00",
                "weekdays": [0],
                "week_of_month": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
