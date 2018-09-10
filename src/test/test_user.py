import json
import unittest

from main import APP


class TestUser(unittest.TestCase):
    def setUp(self):
        self.data = {
            'username': 'dummy',
            'email': 'dummy@test.com',
            'password': '1234'}
        self.wrong_data = {
            'username': 'dummy',
            'email': 'dummy@test.com',
            'password': '4321'}

    def tearDown(self):
        """
        더미 유저 삭제
        """
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.data))

    def test_user_create(self):
        """
        url에서 유저 생성 테스트
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('email'), self.data['email'])

    def test_user_delete(self):
        """
        url에서 유저 올바른 삭제 테스트
        """
        equest, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 204)

    def test_user_wrong_password_delete(self):
        """
        url에서 유저 잘못된 패스워드 삭제 테스트
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.wrong_data))
        self.assertEqual(response.json.get('message'), '유저 정보가 맞지 않습니다.')
        self.assertEqual(response.status, 400)
