import json
import unittest

from main import APP
from src.test.test_values import TestUserValues, TestQuestionValues, TestSelectionValues


class TestSurveyResultAPI(unittest.TestCase):
    """
    설문 결과 API 테스트
    """

    def setUp(self):
        """
        더미 질문, 선택지, 유저 생성
        """
        APP.test_client.post(
            '/survey/question', data=json.dumps(TestQuestionValues.default)
        )

        request, response = APP.test_client.post(
            f'/survey/question/{TestQuestionValues.default["subject"]}/selection',
            data=json.dumps(TestSelectionValues.default)
        )
        self.dummy_selection_value = 'selection-' + str(response.json.get('id'))

        self.data = {
            'question-dummy': self.dummy_selection_value
        }

        request, response = APP.test_client.post(
            '/user', data=json.dumps(TestUserValues.default))
        self.dummy_user_id = response.json['id']

    def tearDown(self):
        """
        더미 질문, 선택지, 유저 삭제
        """
        APP.test_client.delete(
            f'/survey/question/{TestQuestionValues.default["subject"]}'
        )

        APP.test_client.delete(
            f'/user/{TestUserValues.default["username"]}', data=json.dumps(TestUserValues.default))

    def test_survey_result_create_succeed(self):
        """
        url에서 설문 결과 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            f'/survey/result/{self.dummy_user_id}', data=json.dumps(self.data)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('selection'), TestSelectionValues.default['select'])
