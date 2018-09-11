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
        self.patch_data = {
            'username': 'dummy',
            'email': 'chubby@test.com',
            'phone': '01098765432',
            'password': '1234'
        }
        self.wrong_data = {
            'username': 'dummy',
            'email': 'dummy@test.com',
            'phone': '01012345678',
            'password': '4321'
        }
        self.empty_data = {
            'username': '',
            'email': '',
            'phone': '',
            'password': ''
        }

    def tearDown(self):
        """
        더미 유저 삭제
        """
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.data))

    #     유저 생성 테스트     #

    def test_user_create_succeed(self):
        """
        url에서 유저 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('email'), self.data['email'])

    def test_user_create_failed_input_empty(self):
        """
        url에서 유저 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), '정보를 모두 입력해주세요')

    #     유저 수정 테스트     #

    def test_user_patch_succeed(self):
        """
        url에서 유저 정보 수정 테스트 성공
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/user', data=json.dumps(self.patch_data))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('email'), self.patch_data['email'])
        self.assertEqual(response.json.get('phone'), self.patch_data['phone'])

    def test_user_patch_failed_input_empty(self):
        """
        url에서 유저 정보 수정 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.patch(
            '/user', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), '정보를 모두 입력해주세요')

    def test_user_patch_failed_none_user(self):
        """
        url에서 유저 정보 수정 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.patch(
            '/user', data=json.dumps({'username': 'coffee'}))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), '존재하지 않는 유저입니다. 입력값을 확인해주세요')

    #     유저 삭제 테스트     #

    def test_user_delete_succeed(self):
        """
        url에서 유저 삭제 테스트 성공
        """
        equest, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 204)

    def test_user_delete_failed_input_empty(self):
        """
        url에서 유저 삭제 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.empty_data))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), '정보를 모두 입력해주세요')

    def test_user_delete_failed_none_user(self):
        """
        url에서 유저 삭제 테스트 실패: 유저 없음
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/user', data=json.dumps({'username': 'coffee'}))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), '존재하지 않는 유저입니다. 입력값을 확인해주세요')

    def test_user_delete_failed_wrong_password(self):
        """
        url에서 유저 잘못된 패스워드 삭제 테스트
        """
        request, response = APP.test_client.post(
            '/user', data=json.dumps(self.data))
        request, response = APP.test_client.delete(
            '/user', data=json.dumps(self.wrong_data))
        self.assertEqual(response.json.get('message'), '유저 정보가 맞지 않습니다.')
        self.assertEqual(response.status, 400)
