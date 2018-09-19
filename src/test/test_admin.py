import json
import unittest

from main import APP
from common.messages import SUCCEED_MESSAGE, EXCEPTION_MESSAGE


class TestUser(unittest.TestCase):
    def setUp(self):
        self.data = {
            'username': 'admin',
            'password': 'super'
        }
        self.patch_data = {
            'username': 'admin',
            'password': 'abcd'
        }
        self.empty_data = {
            'username': '',
            'password': ''
        }
        self.invalid_password = {
            'username': 'admin',
            'password': '4321'
        }
        self.none_user = {
            'username': 'coffee',
            'password': 'super'
        }

    def tearDown(self):
        """
        더미 유저 삭제
        """
        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(self.data))

    #     유저 생성 테스트     #

    def test_user_create_succeed(self):
        """
        url에서 유저 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)
        self.assertTrue(response.json.get('is_admin'))

    def test_user_create_failed_input_empty(self):
        """
        url에서 유저 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    #     비밀번호 수정 테스트     #

    def test_user_patch_succeed(self):
        """
        url에서 유저 비밀번호 수정 테스트 성공
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(self.patch_data))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), SUCCEED_MESSAGE['patch_password'])

    def test_user_patch_failed_input_empty(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/admin', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_patch_failed_none_user(self):
        """
        url에서 유저 비밀번호 수정 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

    #     유저 삭제 테스트     #

    def test_user_delete_succeed(self):
        """
        url에서 유저 삭제 테스트 성공
        """
        equest, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 204)

    def test_user_delete_failed_input_empty(self):
        """
        url에서 유저 삭제 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_user_delete_failed_none_user(self):
        """
        url에서 유저 삭제 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(self.none_user))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_user'])

    def test_user_delete_failed_wrong_password(self):
        """
        url에서 유저 패스워드 삭제 테스트 실패: 비밀번호 불일치
        """
        request, response = APP.test_client.post(
            '/admin', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/admin', data=json.dumps(self.invalid_password))
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['invalid_password'])
        self.assertEqual(response.status, 400)
