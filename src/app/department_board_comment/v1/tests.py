from rest_framework import status
from rest_framework.test import APITestCase

from app.department.models import Department
from app.department_board.models import DepartmentBoard
from app.department_board_comment.models import DepartmentBoardComment
from app.sub_department.models import SubDepartment
from app.user.models import User, UserGradeChoices


class DepartmentBoardCommentListAPITest(APITestCase):
    MODEL = DepartmentBoardComment
    PATH = "/v1/department_board_comment/"

    def setUp(self) -> None:
        # given
        self.success_user = User.objects.create_user(email="success@test.com")  # TODO: 성공 유저 사전 조건 수정
        self.failure_user = User.objects.create_user(email="failure@test.com")  # TODO: 실패 유저 사전 조건 수정
        self.MODEL.objects.bulk_create([self.MODEL() for i in range(20)])  # TODO: 테스트 데이터 추가

    def test_success_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.get(self.PATH)

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답
        result_keys = []  # TODO: 응답 키 추가
        for data in response.data["results"]:
            self.assertListEqual(
                sorted(result_keys),
                sorted(data.keys()),
            )

    # TODO: 인증이 필요 없는 경우 제거
    def test_failure_response_authentication_failed(self):
        # when
        response = self.client.get(self.PATH)

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: 권한이 필요 없는 경우 제거
    def test_failure_response_permission_failed(self):
        # when
        self.client.force_authenticate(self.failure_user)
        response = self.client.get(self.PATH)

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentBoardCommentCreateAPITest(APITestCase):
    MODEL = DepartmentBoardComment
    PATH = "/v1/department_board_comment/"

    def setUp(self) -> None:
        # given
        self.success_user = User.objects.create_user(email="success@test.com")  # TODO: 성공 유저 사전 조건 수정
        self.failure_user = User.objects.create_user(email="failure@test.com")  # TODO: 실패 유저 사전 조건 수정
        self.MODEL.objects.bulk_create([self.MODEL() for i in range(20)])  # TODO: 테스트 데이터 생성

    def test_success_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.post(self.PATH, data={})  # TODO: 성공 요청 데이터 추가

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 응답
        self.assertDictEqual(response.data, {})  # TODO: 응답 데이터 추가

        # 디비
        self.assertTrue(self.MODEL.objects.filter(id=response.data["id"]).exists())

    def test_failure_response_invalid_failed(self):
        # when
        response = self.client.post(self.PATH, data={})  # TODO: 실패 요청 데이터 추가

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 응답
        self.assertDictEqual(response.data, {})  # TODO: 응답 데이터 추가

        # 디비
        self.assertFalse(self.MODEL.objects.filter(id=response.data["id"]).exists())

    # TODO: 인증이 필요 없는 경우 제거
    def test_failure_response_authentication_failed(self):
        # when
        response = self.client.get(self.PATH)

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: 권한이 필요 없는 경우 제거
    def test_failure_response_permission_failed(self):
        # when
        self.client.force_authenticate(self.failure_user)
        response = self.client.get(self.PATH)

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentBoardCommentRetrieveAPITest(APITestCase):
    MODEL = DepartmentBoardComment
    PATH = "/v1/department_board_comment/{id}/"

    def setUp(self) -> None:
        # given
        self.success_user = User.objects.create_user(email="success@test.com")  # TODO: 성공 유저 사전 조건 수정
        self.failure_user = User.objects.create_user(email="failure@test.com")  # TODO: 실패 유저 사전 조건 수정
        self.instance = self.MODEL.objects.create()  # TODO: 테스트 데이터 생성

    def test_success_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상대값
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답
        self.assertDictEqual(response.data, {})  # TODO: 응답 데이터 추가

    # TODO: 인증이 필요 없는 경우 제거
    def test_failure_response_authentication_failed(self):
        # when
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: 권한이 필요 없는 경우 제거
    def test_failure_response_permission_failed(self):
        # when
        self.client.force_authenticate(self.failure_user)
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentBoardCommentUpdateAPITest(APITestCase):
    MODEL = DepartmentBoardComment
    PATH = "/v1/department_board_comment/{id}/"

    def setUp(self) -> None:
        # given
        self.success_user = User.objects.create_user(email="success@test.com")  # TODO: 성공 유저 사전 조건 수정
        self.failure_user = User.objects.create_user(email="failure@test.com")  # TODO: 실패 유저 사전 조건 수정
        self.instance = self.MODEL.objects.create()  # TODO: 테스트 데이터 생성

    def test_success_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.put(self.PATH.format(id=self.instance.id), data={})  # TODO: 성공 요청 데이터 추가

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답
        self.assertDictEqual(response.data, {})  # TODO: 응답 데이터 추가

        # 디비
        self.assertFalse(self.MODEL.objects.filter(id=self.instance.id).exists())

    def test_failure_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.put(self.PATH.format(id=self.instance.id), data={})  # TODO: 실패 요청 데이터 추가

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 응답
        self.assertDictEqual(response.data, {})  # TODO: 응답 데이터 추가

    # TODO: 인증이 필요 없는 경우 제거
    def test_failure_response_authentication_failed(self):
        # when
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: 권한이 필요 없는 경우 제거
    def test_failure_response_permission_failed(self):
        # when
        self.client.force_authenticate(self.failure_user)
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentBoardCommentDestroyAPITest(APITestCase):
    MODEL = DepartmentBoardComment
    PATH = "/v1/department_board_comment/{id}/"

    def setUp(self) -> None:
        # given
        self.success_user = User.objects.create_user(email="success@test.com")  # TODO: 성공 유저 사전 조건 수정
        self.failure_user = User.objects.create_user(email="failure@test.com")  # TODO: 실패 유저 사전 조건 수정
        self.instance = self.MODEL.objects.create()  # TODO: 성공 테스트 데이터 생성

    def test_success_response(self):
        # when
        self.client.force_authenticate(self.success_user)  # TODO: 인증이 필요 없는 경우 제거
        response = self.client.delete(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 응답
        self.assertIsNone(response.data)

        # 디비
        self.assertFalse(self.MODEL.objects.filter(id=self.instance.id).exists())

    # TODO: 인증이 필요 없는 경우 제거
    def test_failure_response_authentication_failed(self):
        # when
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: 권한이 필요 없는 경우 제거
    def test_failure_response_permission_failed(self):
        # when
        self.client.force_authenticate(self.failure_user)
        response = self.client.get(self.PATH.format(id=self.instance.id))

        # then
        # 상태값
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DepartmentBoardCommentOrderingTest(APITestCase):
    """댓글 오래된 순(created_at 오름차순) 정렬 테스트"""

    PATH = "/v1/department_board/{board_id}/comment/"

    def setUp(self):
        self.department = Department.objects.create(name="테스트분과")
        self.sub_department = SubDepartment.objects.create(department=self.department, name="테스트세부분과")
        self.user = User.objects.create(
            email="user@test.com",
            password="test1234",
            name="테스트유저",
            baptismal_name="요한",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_06,
            is_active=True,
        )
        self.user.sub_department_set.add(self.sub_department)
        self.board = DepartmentBoard.objects.create(
            user=self.user,
            department=self.department,
            sub_department=self.sub_department,
            title="테스트게시글",
            body="본문",
        )
        self.comment_1 = DepartmentBoardComment.objects.create(
            user=self.user,
            department_board=self.board,
            body="첫 번째 댓글",
        )
        self.comment_2 = DepartmentBoardComment.objects.create(
            user=self.user,
            department_board=self.board,
            body="두 번째 댓글",
        )
        self.comment_3 = DepartmentBoardComment.objects.create(
            user=self.user,
            department_board=self.board,
            body="세 번째 댓글",
        )

    def test_comments_ordered_oldest_first(self):
        """댓글이 오래된 순(id 오름차순)으로 반환되는지 확인"""
        self.client.force_authenticate(self.user)
        response = self.client.get(self.PATH.format(board_id=self.board.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [comment["id"] for comment in response.data["results"]]
        self.assertEqual(ids, sorted(ids), "댓글이 오래된 순으로 정렬되지 않음")
