from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from common.validation import Validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Question

blueprint = Blueprint('SurveyQuestion')


class SurveyQuestionView(HTTPMethodView):
    """
    설문조사: 질문 메서드 집합
    1. POST: 질문 생성
    2. DELETE: 질문 삭제
    """

    async def post(self, request):
        """
        질문 생성
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        question = Question(**data)
        db_session.add(question)
        db_session.commit()
        db_session.flush()
        db_session.close()

        query_question = Validation.query_validation(db_session, Question, title=data['title'])

        return json({
            'subject': query_question.subject,
            'title': query_question.title
        }, status=201)

    async def delete(self, request):
        """
        질문 삭제
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        query_question = Validation.query_validation(db_session, Question, title=data['title'])
        if query_question is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        db_session.delete(query_question)
        db_session.commit()
        db_session.flush()
        db_session.close()

        return json(None, status=204)


blueprint.add_route(SurveyQuestionView.as_view(), '/survey/question', strict_slashes=True)
