from rest_framework import status
from rest_framework.test import APITestCase

from app.department.models import Department
from app.department_board.models import DepartmentBoard
from app.sub_department.models import SubDepartment
from app.user.models import User, UserGradeChoices


class DepartmentBoardPinLimitAPITest(APITestCase):
    """분과 게시판 고정글 최대 5개 제한 테스트"""

    PATH = "/v1/department_board/"

    def setUp(self):
        # 분과/세부분과 생성
        self.department = Department.objects.create(name="테스트분과")
        self.sub_department = SubDepartment.objects.create(department=self.department, name="테스트세부분과")
        self.sub_department_2 = SubDepartment.objects.create(department=self.department, name="다른세부분과")

        # 다른 분과 (격리 테스트용)
        self.other_department = Department.objects.create(name="다른분과")
        self.other_sub_department = SubDepartment.objects.create(
            department=self.other_department, name="다른분과세부분과"
        )

        # 단체장(GRADE_04) - 고정글 권한 있음
        self.user = User.objects.create(
            email="leader@test.com",
            password="test1234",
            name="단체장",
            baptismal_name="요한",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_04,
            is_active=True,
        )
        self.user.sub_department_set.add(self.sub_department, self.sub_department_2, self.other_sub_department)

        # 일반 신자(GRADE_06) - 고정글 권한 없음
        self.normal_user = User.objects.create(
            email="normal@test.com",
            password="test1234",
            name="일반신자",
            baptismal_name="바오로",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_06,
            is_active=True,
        )
        self.normal_user.sub_department_set.add(self.sub_department)

    def _create_board(self, user, sub_department, is_fixed=False, title="테스트"):
        """게시글 생성 헬퍼"""
        self.client.force_authenticate(user)
        return self.client.post(
            self.PATH,
            data={
                "sub_department": sub_department.id,
                "title": title,
                "body": "<p>테스트 본문</p>",
                "is_fixed": is_fixed,
            },
            format="json",
        )

    def test_pin_1_to_5_success(self):
        """고정글 1~5개까지 등록 성공"""
        for i in range(1, 6):
            response = self._create_board(self.user, self.sub_department, is_fixed=True, title=f"고정글{i}")
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f"{i}번째 고정글 등록 실패: {response.data}",
            )

        # DB에 고정글 5개 확인 (분과 기준)
        pinned_count = DepartmentBoard.objects.filter(department=self.department, is_fixed=True).count()
        self.assertEqual(pinned_count, 5)

    def test_pin_6th_fail(self):
        """6번째 고정글 등록 시 실패"""
        # 5개 먼저 생성
        for i in range(5):
            DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )

        # 6번째 시도
        response = self._create_board(self.user, self.sub_department, is_fixed=True, title="고정글6")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is_fixed", response.data)

    def test_pin_same_department_sub_departments_share_limit(self):
        """같은 분과 내 세부분과들은 고정글 한도를 공유"""
        # sub_department에 5개 고정
        for i in range(5):
            DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )

        # 같은 분과의 sub_department_2에는 더 이상 고정글 등록 불가
        response = self._create_board(self.user, self.sub_department_2, is_fixed=True, title="같은분과고정글")
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
            f"같은 분과 내 6번째 고정글이 허용됨 (정책 위반): {response.data}",
        )
        self.assertIn("is_fixed", response.data)

    def test_pin_different_department_independent(self):
        """다른 분과의 고정글은 별도로 카운트"""
        # department에 5개 고정
        for i in range(5):
            DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )

        # other_department에는 고정 가능
        response = self._create_board(self.user, self.other_sub_department, is_fixed=True, title="타분과고정글")
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"다른 분과에 고정글 등록 실패: {response.data}",
        )

    def test_unpin_then_pin_new_one(self):
        """고정 해제 후 새 고정글 등록 가능"""
        # 5개 고정
        boards = []
        for i in range(5):
            board = DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )
            boards.append(board)

        # 첫 번째 고정 해제
        self.client.force_authenticate(self.user)
        response = self.client.put(
            f"{self.PATH}{boards[0].id}/",
            data={
                "sub_department": self.sub_department.id,
                "title": boards[0].title,
                "body": boards[0].body,
                "is_fixed": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, f"고정 해제 실패: {response.data}")

        # 새 고정글 등록
        response = self._create_board(self.user, self.sub_department, is_fixed=True, title="새고정글")
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"고정 해제 후 새 고정글 등록 실패: {response.data}",
        )

    def test_update_existing_pinned_post_no_count_issue(self):
        """이미 고정된 게시글 수정 시 자기 자신 제외하여 카운트"""
        # 5개 고정
        boards = []
        for i in range(5):
            board = DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )
            boards.append(board)

        # 기존 고정 게시글 제목만 수정 (is_fixed=True 유지)
        self.client.force_authenticate(self.user)
        response = self.client.put(
            f"{self.PATH}{boards[0].id}/",
            data={
                "sub_department": self.sub_department.id,
                "title": "수정된 고정글",
                "body": "수정된 본문",
                "is_fixed": True,
            },
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"기존 고정글 수정 실패: {response.data}",
        )

    def test_non_pinned_post_not_affected_by_limit(self):
        """고정되지 않은 일반 게시글은 제한에 영향 없음"""
        # 5개 고정
        for i in range(5):
            DepartmentBoard.objects.create(
                user=self.user,
                department=self.department,
                sub_department=self.sub_department,
                title=f"고정글{i + 1}",
                body="본문",
                is_fixed=True,
            )

        # 일반 게시글은 여전히 등록 가능
        response = self._create_board(self.user, self.sub_department, is_fixed=False, title="일반글")
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"일반 게시글 등록 실패: {response.data}",
        )

    def test_normal_user_cannot_pin(self):
        """권한 없는 유저(GRADE_06)는 고정글 등록 불가"""
        response = self._create_board(self.normal_user, self.sub_department, is_fixed=True, title="무권한고정시도")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("is_fixed", response.data)


class DepartmentBoardPermissionTest(APITestCase):
    """분과게시판 조회 권한 테스트"""

    LIST_PATH = "/v1/department_board/"
    DETAIL_PATH = "/v1/department_board/{id}/"

    def setUp(self):
        # 총관리자 (GRADE_01)
        self.admin = User.objects.create(
            email="admin@test.com",
            password="test1234",
            name="총관리자",
            baptismal_name="미카엘",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_01,
            is_active=True,
        )

        # A 분과
        self.department_a = Department.objects.create(name="A분과")
        self.sub_dept_a = SubDepartment.objects.create(department=self.department_a, name="A세부분과")

        # B 분과
        self.department_b = Department.objects.create(name="B분과")
        self.sub_dept_b = SubDepartment.objects.create(department=self.department_b, name="B세부분과")

        # A분과 소속 본당 신자 (GRADE_06)
        self.user_a = User.objects.create(
            email="user_a@test.com",
            password="test1234",
            name="A분과신자",
            baptismal_name="요한",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_06,
            is_active=True,
        )
        self.user_a.sub_department_set.add(self.sub_dept_a)

        # B분과 소속 본당 신자 (GRADE_06)
        self.user_b = User.objects.create(
            email="user_b@test.com",
            password="test1234",
            name="B분과신자",
            baptismal_name="베드로",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_06,
            is_active=True,
        )
        self.user_b.sub_department_set.add(self.sub_dept_b)

        # 타본당 신자 (GRADE_07)
        self.user_grade07 = User.objects.create(
            email="guest@test.com",
            password="test1234",
            name="타본당신자",
            baptismal_name="안드레아",
            postcode="12345",
            base_address="서울",
            detail_address="강남",
            birth="1990-01-01",
            grade=UserGradeChoices.GRADE_07,
            is_active=True,
        )

        # B분과 일반글
        self.board_b_public = DepartmentBoard.objects.create(
            user=self.user_b,
            department=self.department_b,
            sub_department=self.sub_dept_b,
            title="B분과 일반글",
            body="본문",
            is_secret=False,
        )

        # B분과 비밀글
        self.board_b_secret = DepartmentBoard.objects.create(
            user=self.user_b,
            department=self.department_b,
            sub_department=self.sub_dept_b,
            title="B분과 비밀글",
            body="본문",
            is_secret=True,
        )

    # --- GRADE_07 접근 차단 ---

    def test_grade07_cannot_list(self):
        """타본당 신자(GRADE_07)는 목록 조회 불가"""
        self.client.force_authenticate(self.user_grade07)
        response = self.client.get(self.LIST_PATH, {"department": self.department_b.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_grade07_cannot_retrieve(self):
        """타본당 신자(GRADE_07)는 상세 조회 불가"""
        self.client.force_authenticate(self.user_grade07)
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_public.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- 타분과 일반글 열람 ---

    def test_other_department_user_can_list_public_posts(self):
        """타분과 소속 유저도 일반글 목록 조회 가능"""
        self.client.force_authenticate(self.user_a)
        response = self.client.get(self.LIST_PATH, {"department": self.department_b.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [post["id"] for post in response.data["results"]]
        self.assertIn(self.board_b_public.id, ids)

    def test_other_department_user_can_retrieve_public_post(self):
        """타분과 소속 유저도 일반글 상세 조회 가능"""
        self.client.force_authenticate(self.user_a)
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_public.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- 비밀글 접근 제한 ---

    def test_other_department_user_cannot_see_secret_post_in_list(self):
        """타분과 소속 유저는 목록에서 비밀글 미노출"""
        self.client.force_authenticate(self.user_a)
        response = self.client.get(self.LIST_PATH, {"department": self.department_b.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [post["id"] for post in response.data["results"]]
        self.assertNotIn(self.board_b_secret.id, ids)

    def test_other_department_user_cannot_retrieve_secret_post(self):
        """타분과 소속 유저는 비밀글 상세 조회 불가"""
        self.client.force_authenticate(self.user_a)
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_secret.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_same_sub_department_user_can_retrieve_secret_post(self):
        """동일 세부분과 소속 유저는 비밀글 상세 조회 가능"""
        self.client.force_authenticate(self.user_b)
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_secret.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- 비인증 ---

    def test_unauthenticated_cannot_retrieve(self):
        """비인증 유저는 상세 조회 불가"""
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_public.id))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- 총관리자 ---

    def test_admin_can_retrieve_any_secret_post(self):
        """총관리자(GRADE_01)는 타분과 비밀글도 상세 조회 가능"""
        self.client.force_authenticate(self.admin)
        response = self.client.get(self.DETAIL_PATH.format(id=self.board_b_secret.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DepartmentBoardListAPITest(APITestCase):
    MODEL = DepartmentBoard
    PATH = "/v1/department_board/"

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


class DepartmentBoardCreateAPITest(APITestCase):
    MODEL = DepartmentBoard
    PATH = "/v1/department_board/"

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


class DepartmentBoardRetrieveAPITest(APITestCase):
    MODEL = DepartmentBoard
    PATH = "/v1/department_board/{id}/"

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


class DepartmentBoardUpdateAPITest(APITestCase):
    MODEL = DepartmentBoard
    PATH = "/v1/department_board/{id}/"

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


class DepartmentBoardDestroyAPITest(APITestCase):
    MODEL = DepartmentBoard
    PATH = "/v1/department_board/{id}/"

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
