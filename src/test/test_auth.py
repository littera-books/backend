import json
import unittest

from main import APP


class TestAuth(unittest.TestCase):
    def setUp(self):
        self.data = {
            'username': 'authy',
            'email': 'authy@test.com',
            'phone': '01024681357',
            'password': '1234'}

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

    def test_user_login_failed_input_empty(self):
        """
        url에서 실패한 로그인 테스트: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth', data=json.dumps({
                'username': '',
                'password': ''
            }))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], '아이디나 비밀번호를 입력해주세요')

    def test_user_login_failed_user_none(self):
        """
        url에서 실패한 로그인 테스트: 유저 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth', data=json.dumps({
                'username': 'littera',
                'password': '1234'
            }))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], '유저 정보가 존재하지 않습니다')

    def test_user_login_failed_password_diff(self):
        """
        url에서 실패한 로그인 테스트: 비밀번호 불일치
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.post(
            '/auth', data=json.dumps({
                'username': 'authy',
                'password': '4321'
            }))
        self.assertEqual(response.status, 401)
        self.assertEqual(response.json['reasons'][0], '비밀번호가 일치하지 않습니다')
