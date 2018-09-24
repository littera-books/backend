from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Question

blueprint = Blueprint('SurveyQuestion')


class QuestionCreateListView(HTTPMethodView):

    async def get(self, request):
        """
        질문 리스트 반환
        """
        query_question = db_session.query(Question).order_by(Question.created_at).all()

        result = {
            'length': len(query_question),
            'items': []
        }

        for question in query_question:
            item = {
                'id': question.id,
                'subject': question.subject,
                'title': question.title
            }
            result['items'].append(item)

        return json(result, status=200)

    async def post(self, request):
        """
        질문 생성
        """
        data = request.json

        is_full = empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        subject_length = length_validation(data['subject'], 50)
        if subject_length is False:
            return json({'message': EXCEPTION_MESSAGE['invalid_subject']}, status=400)

        question = Question(**data)
        db_session.add(question)
        db_session.commit()
        db_session.flush()
        db_session.close()

        query_question = query_validation(db_session, Question, subject=data['subject'])

        return json({
            'subject': query_question.subject,
            'title': query_question.title
        }, status=201)


class QuestionRetrieveUpdateDeleteView(HTTPMethodView):

    async def delete(self, request, subject):
        """
        질문 삭제
        """

        query_question = query_validation(db_session, Question, subject=subject)
        if query_question is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        db_session.delete(query_question)
        db_session.commit()
        db_session.flush()
        db_session.close()

        return json(None, status=204)


blueprint.add_route(QuestionCreateListView.as_view(), '/survey/question', strict_slashes=True)
blueprint.add_route(QuestionRetrieveUpdateDeleteView.as_view(), '/survey/question/<subject>', strict_slashes=True)
