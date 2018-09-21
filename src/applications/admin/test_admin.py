import json
import unittest

from main import APP
from common.messages import SUCCEED_MESSAGE, EXCEPTION_MESSAGE
from src.test.test_values import TestAdminValues


class TestAdminAPI(unittest.TestCase):
    """
    관리자 API CRUD 테스트
    """

    def tearDown(self):
        """
        더미 유저 삭제
        """
        APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.default))

    #     유저 생성 테스트     #

    def test_user_create_succeed(self):
        """
        url에서 유저 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)
        self.assertTrue(response.json.get('is_admin'))

    def test_user_create_failed_input_empty(self):
        """
        url에서 유저 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    #     비밀번호 수정 테스트     #

    def test_user_patch_succeed(self):
        """
        url에서 유저 비밀번호 수정 테스트 성공
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(TestAdminValues.patch))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

    def test_user_patch_failed_input_empty(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(TestAdminValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_patch_failed_none_user(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

    #     유저 삭제 테스트     #

    def test_user_delete_succeed(self):
        """
        url에서 유저 삭제 테스트 성공
        """
        equest, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 204)

    def test_user_delete_failed_input_empty(self):
        """
        url에서 유저 삭제 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_delete_failed_none_user(self):
        """
        url에서 유저 삭제 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.none))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_user'])

    def test_user_delete_failed_wrong_password(self):
        """
        url에서 유저 패스워드 삭제 테스트 실패: 비밀번호 불일치
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.invalid_password))
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['invalid_password'])
        self.assertEqual(response.status, 400)


class TestAdminAuth(unittest.TestCase):
    """
    관리자 authentication 테스트
    """

    def tearDown(self):
        """
        더미 유저 삭제
        """
        APP.test_client.delete(
            '/admin', data=json.dumps(TestAdminValues.default))

    def test_user_login_succeed(self):
        """
        url에서 올바른 로그인 테스트
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 200)

    def test_user_login_failed_input_empty(self):
        """
        url에서 실패한 로그인 테스트: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth/admin', data=json.dumps(TestAdminValues.empty))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['empty_value'])

    def test_user_login_failed_user_none(self):
        """
        url에서 실패한 로그인 테스트: 유저 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth/admin', data=json.dumps(TestAdminValues.none))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['none_user'])

    def test_user_login_failed_password_diff(self):
        """
        url에서 실패한 로그인 테스트: 비밀번호 불일치
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(TestAdminValues.default))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth/admin', data=json.dumps(TestAdminValues.invalid_password))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['invalid_password'])
