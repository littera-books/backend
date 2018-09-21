import json
import unittest

from main import APP
from common.messages import EXCEPTION_MESSAGE
from src.test.test_values import TestQuestionValues


class TestQuestionAPI(unittest.TestCase):
    """
    설문조사 API CRUD 테스트
    """

    def tearDown(self):
        """
        더미 질문 삭제
        """
        APP.test_client.delete(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )

    #     질문 생성 테스트     #

    def test_question_create_succeed(self):
        """
        url에서 질문 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('subject'), TestQuestionValues.default['subject'])

    def test_question_create_failed_input_empty(self):
        """
        url에서 질문 생성 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.empty)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    #     질문 삭제 테스트     #

    def test_question_delete_succeed(self):
        """
        url에서 질문 삭제 테스트 성공
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 204)

    def test_question_delete_failed_input_empty(self):
        """
        url에서 질문 삭제 테스트 실패: 입력값 없음
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/survey/question', data=json.dumps(TestQuestionValues.empty)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['empty_value'])

    def test_question_delete_failed_none_question(self):
        """
        url에서 질문 삭제 테스트 실패: 질문 없음
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.assertEqual(response.status, 201)

        request, response = APP.test_client.delete(
            '/survey/question', data=json.dumps(TestQuestionValues.none)
        )
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json.get('message'), EXCEPTION_MESSAGE['none_question'])
