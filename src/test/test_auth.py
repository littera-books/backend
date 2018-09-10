import json
import unittest

from main import APP


class TestUser(unittest.TestCase):
    def setUp(self):
        self.data = {
            'username': 'dummy',
            'email': 'dummy@test.com',
            'phone': '01012345678',
            'password': '1234'}

        self.wrong_data = {
            'username': 'dummy',
            'password': '4321'}

    def tearDown(self):
        """
        더미 유저 삭제
        """
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.data))

    def test_user_login_success(self):
        """
        url에서 올바른 로그인 테스트
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth', data=json.dumps(self.data))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('message'), 'ok')

    def test_user_login_failed(self):
        """
        url에서 실패한 로그인 테스트
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth', data=json.dumps(self.wrong_data))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json.get('message'), '유저 정보가 맞지 않습니다.')
