import json
import unittest

from main import APP
from common.messages import EXCEPTION_MESSAGE
from src.test.test_values import TestQuestionValues, TestSelectionValues


class TestSelectionAPI(unittest.TestCase):
    """
    설문조사 질문의 선택지 API CRUD 테스트
    """

    def setUp(self):
        """
        더미 질문 생성
        """
        request, response = APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )
        self.question_id = response.json.get('id')

    def tearDown(self):
        """
        더미 질문 삭제
        """
        APP.test_client.delete(
            f'/survey/question/{self.question_id}')

    #     선택지 생성 테스트     #

    def test_selection_succeed(self):
        """
        url로 선택지 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            f'/survey/question/{self.question_id}/selection',
            data=json.dumps(TestSelectionValues.default)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('select'), TestSelectionValues.default['select'])

    #     선택지 디테일 테스트     #

    def test_selection_retrieve_succeed(self):
        """
        url로 선택지 디테일 불러오기 테스트 성공
        """
        request, response = APP.test_client.post(
            f'/survey/question/{self.question_id}/selection',
            data=json.dumps(TestSelectionValues.default)
        )
        self.assertEqual(response.status, 201)

        selection_id = response.json.get('id')

        request, response = APP.test_client.get(
            f'/survey/question/{self.question_id}/selection/{selection_id}'
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json.get('id'), selection_id)

    #     선택지 삭제 테스트     #

    def test_selection_delete_succeed(self):
        """
        url로 선택지 삭제 테스트 성공
        """
        request, response = APP.test_client.post(
            f'/survey/question/{self.question_id}/selection',
            data=json.dumps(TestSelectionValues.default)
        )
        self.assertEqual(response.status, 201)

        selection_id = response.json.get('id')

        request, response = APP.test_client.delete(
            f'/survey/question/{self.question_id}/selection/{selection_id}'
        )
        self.assertEqual(response.status, 204)
