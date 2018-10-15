import json
import unittest

from main import APP
from common.messages import EXCEPTION_MESSAGE
from src.test.test_values import TestQuestionValues


class TestQuestionCreateAPI(unittest.TestCase):
    """
    설문조사 생성 API 테스트
    """

    def test_question_create_succeed(self):
        """
        url에서 질문 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('subject'), TestQuestionValues.default['subject'])
        self.question_id = response.json.get('id')

        request, response = APP.test_client.delete(
            f'/survey/question/{self.question_id}'
        )
        self.assertEqual(response.status, 204)

    def test_question_create_failed_input_empty(self):
        """
        url에서 질문 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.empty)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])


class TestQuestionAPI(unittest.TestCase):
    """
    설문조사 API CRUD 테스트
    """

    def setUp(self):
        """
        더미 질문 생성
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)
        self.question_id = response.json.get('id')

    def tearDown(self):
        """
        더미 질문 삭제
        """
        APP.test_client.delete(
            f'/survey/question/{self.question_id}')

    #     질문 호출 테스트     #
    def test_question_get_list(self):
        """
        url에서 질문 호출 테스트 성공
        """
        request, response = APP.test_client.get('/survey/question')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('length'), len(response.json.get('items')))

    #     질문 디테일 테스트     #

    def test_question_retrieve_succeed(self):
        """
        url에서 질문 디테일 테스트 성공
        """
        request, response = APP.test_client.get(
            f'/survey/question/{self.question_id}')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('subject'), TestQuestionValues.default['subject'])

    def test_question_retrieve_failed_input_empty(self):
        """
        url에서 질문 디테일 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.get(
            '/survey/question/')
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_question_retrieve_failed_none_question(self):
        """
        url에서 질문 디테일 테스트 실패: 질문 없음
        """
        request, response = APP.test_client.get(
            '/survey/question/0')
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_question'])

    #     질문 수정 테스트     #

    def test_question_put_succeed(self):
        """
        url에서 질문 수정 테스트 성공
        """
        request, response = APP.test_client.put(
            f'/survey/question/{self.question_id}',
            data=json.dumps(TestQuestionValues.put))
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('title'), TestQuestionValues.put['title'])

    def test_question_put_failed_input_empty(self):
        """
        url에서 질문 수정 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.put(
            '/survey/question/',
            data=json.dumps(TestQuestionValues.put))
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_question_put_test_failed_none_question(self):
        """
        url에서 질문 수정 테스트 실패: 질문 없음
        """
        request, response = APP.test_client.put(
            '/survey/question/0',
            data=json.dumps(TestQuestionValues.put))
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_question'])

    #     질문 삭제 테스트     #

    def test_question_delete_succeed(self):
        """
        url에서 질문 삭제 테스트 성공
        """
        request, response = APP.test_client.delete(
            f'/survey/question/{self.question_id}')
        self.assertEqual(response.status, 204)

    def test_question_delete_failed_input_empty(self):
        """
        url에서 질문 삭제 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.delete(
            '/survey/question/')
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')

    def test_question_delete_failed_none_question(self):
        """
        url에서 질문 삭제 테스트 실패: 질문 없음
        """
        request, response = APP.test_client.delete(
            f'/survey/question/0')
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_question'])
