import json
import unittest

from main import APP
from common.messages import SUCCEED_MESSAGE, EXCEPTION_MESSAGE
from src.test.test_values import TestUserValues


class TestUserCreateAPI(unittest.TestCase):
    """
    유저 API CRUD 테스트: 생성
    """
    def test_user_create_succeed(self):
        """
        url에서 유저 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json['email'], TestUserValues.default['email'])
        self.user_id = response.json['id']
        APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.default))

    def test_user_create_failed_input_empty(self):
        """
        url에서 유저 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['message'], EXCEPTION_MESSAGE['empty_value'])

    def test_user_create_failed_invalid_phone(self):
        """
        url에서 유저 생성 테스트 실패: 휴대폰 번호 길이 초과
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.invalid_phone))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['message'], EXCEPTION_MESSAGE['invalid_phone'])


class TestUserUpdateDestroyAPI(unittest.TestCase):
    """
    유저 API CRUD 테스트: 수정, 삭제
    """
    def setUp(self):
        """
        더미 유저 생성
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 201)
        self.user_id = response.json['id']

    def tearDown(self):
        """
        더미 유저 삭제
        """
        APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.default))

    #     유저 수정 테스트     #

    def test_user_put_succeed(self):
        """
        url에서 유저 정보 수정 테스트 성공
        """
        request, response = APP.test_client.put(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.put))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['email'], TestUserValues.put['email'])

    def test_user_put_failed_input_url_empty(self):
        """
        url에서 유저 정보 수정 테스트 실패: url 입력값 없음
        """
        request, response = APP.test_client.put(
            f'/user/', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_user_put_failed_input_value_empty(self):
        """
        url에서 유저 정보 수정 테스트 실패: 수정 입력값 없음
        """
        request, response = APP.test_client.put(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_put_failed_invalid_phone(self):
        """
        url에서 유저 정보 수정 테스트 실패: 휴대폰 번호 길이 초과
        """
        request, response = APP.test_client.put(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.invalid_phone))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['invalid_phone'])

    def test_user_put_failed_none_user(self):
        """
        url에서 유저 정보 수정 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.put(
            f'/user/0', data=json.dumps(TestUserValues.none))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_user'])

    #     비밀번호 수정 테스트     #

    def test_user_patch_succeed(self):
        """
        url에서 유저 비밀번호 수정 테스트 성공
        """
        request, response = APP.test_client.patch(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.patch))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

        request, response = APP.test_client.patch(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

    def test_user_patch_failed_input_url_empty(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: url 입력값 없음
        """
        request, response = APP.test_client.patch(
            f'/user/', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_user_patch_failed_input_value_empty(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 수정 입력값 없음
        """
        request, response = APP.test_client.patch(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_patch_failed_none_user(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.patch(
            f'/user/0', data=json.dumps(TestUserValues.none))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_user'])

    #     유저 삭제 테스트     #

    def test_user_delete_succeed(self):
        """
        url에서 유저 삭제 테스트 성공
        """
        request, response = APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 204)

    def test_user_delete_failed_input_url_empty(self):
        """
        url에서 유저 삭제 테스트 실패: url 입력값 없음
        """
        request, response = APP.test_client.delete(
            f'/user/', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_user_delete_failed_input_value_empty(self):
        """
        url에서 유저 삭제 테스트 실패: 삭제 입력값 없음
        """
        request, response = APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_delete_failed_none_user(self):
        """
        url에서 유저 삭제 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.delete(
            f'/user/0', data=json.dumps(TestUserValues.none))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_user'])

    def test_user_delete_failed_wrong_password(self):
        """
        url에서 유저 패스워드 삭제 테스트 실패: 비밀번호 불일치
        """
        request, response = APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.invalid_password))
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['invalid_password'])
        self.assertEqual(response.status, 400)


class TestUserAuth(unittest.TestCase):
    """
    유저 authentication 테스트
    """
    def setUp(self):
        """
        더미 유저 생성
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 201)
        self.user_id = response.json['id']

    def tearDown(self):
        """
        더미 유저 삭제
        """
        APP.test_client.delete(
            f'/user/{self.user_id}', data=json.dumps(TestUserValues.default))

    def test_user_login_success(self):
        """
        url에서 올바른 로그인 테스트
        """
        request, response = APP.test_client.post(
            '/auth/user', data=json.dumps(TestUserValues.default))
        self.assertEqual(response.status, 200)

    def test_user_login_failed_input_empty(self):
        """
        url에서 실패한 로그인 테스트: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/auth/user', data=json.dumps(TestUserValues.empty))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['empty_value'])

    def test_user_login_failed_user_none(self):
        """
        url에서 실패한 로그인 테스트: 유저 없음
        """
        request, response = APP.test_client.post(
            '/auth/user', data=json.dumps(TestUserValues.none))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['none_user'])

    def test_user_login_failed_password_diff(self):
        """
        url에서 실패한 로그인 테스트: 비밀번호 불일치
        """
        request, response = APP.test_client.post(
            '/auth/user', data=json.dumps(TestUserValues.invalid_password))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], EXCEPTION_MESSAGE['invalid_password'])
