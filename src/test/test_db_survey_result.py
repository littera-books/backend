import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database import Base
from applications.user.model import User
from applications.admin.model import Admin
from applications.survey.model import Question, Selection, SurveyResult, ResignSurvey
from .test_values import TestUserValues, TestAdminValues, TestQuestionValues, TestSelectionValues, TestResignSurveyValues


class TestDBSurveyResult(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        self.base = Base
        Base.metadata.create_all(bind=self.engine)

        dummy_admin = Admin(**TestAdminValues.default)
        self.session.add(dummy_admin)

        dummy_user = User(**TestUserValues.default)
        self.session.add(dummy_user)

        dummy_question = Question(**TestQuestionValues.default)
        dummy_selection = Selection(**TestSelectionValues.default)
        dummy_question.selection.append(dummy_selection)

        self.session.add(dummy_question)
        self.session.commit()

    def test_survey_result_create_succeed(self):
        """
        설문 결과 생성 테스트 성공
        """
        query_user = self.session.query(User).filter_by(email=TestUserValues.default['email']).one()
        query_selection = self.session.query(Selection).filter_by(select=TestSelectionValues.default['select']).one()

        dummy_survey_result = SurveyResult()
        dummy_survey_result.user_id = query_user.id
        dummy_survey_result.selection_id = query_selection.id

        self.session.add(dummy_survey_result)
        self.session.commit()

        query_survey_result = self.session.query(SurveyResult).filter(SurveyResult.user_id == query_user.id).one()
        self.assertEqual(query_survey_result.selection.select, TestSelectionValues.default['select'])


class TestDBResignSurvey(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        self.base = Base
        Base.metadata.create_all(bind=self.engine)

    def test_resign_survey_create_succeed(self):
        """
        탈퇴 설문 생성 테스트 성공
        """
        dummy_resign_survey = ResignSurvey(**TestResignSurveyValues.default)

        self.session.add(dummy_resign_survey)
        self.session.commit()

        query_resign_survey = self.session.query(ResignSurvey).first()
        self.assertEqual(query_resign_survey.content, TestResignSurveyValues.default['content'])
