from datetime import date, time

from rest_framework import status
from rest_framework.test import APITestCase

from app.room_reservation.models import CatechismRoom, RoomReservation
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
            "room",
            "room_name",
            "repeat",
            "title",
            "user_name",
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
                "room": self.room.id,
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
                "room": self.room.id,
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
                "room": self.room.id,
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
