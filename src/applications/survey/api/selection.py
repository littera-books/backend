from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Question, Selection

blueprint = Blueprint('SurveySelection')


class SelectionCreateListView(HTTPMethodView):

    async def get(self, request, subject):
        """
        선택지 호출
        """
        query_question = query_validation(db_session, Question, subject=subject)
        if query_question is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        result = {
            'length': len(query_question.selection),
            'items': []
        }

        for selection in query_question.selection:
            item = {
                'id': selection.id,
                'select': selection.select
            }
            result['items'].append(item)

        return json(result, status=200)

    async def post(self, request, subject):
        """
        선택지 생성
        """
        data = request.json

        is_full = empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        query_question = query_validation(db_session, Question, subject=subject)
        if query_question is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        query_question.selection.append(Selection(**data))
        db_session.add(query_question)
        db_session.commit()
        db_session.flush()

        return json({
            'question_subject': query_question.subject,
            'id': query_question.selection[-1].id,
            'select': query_question.selection[-1].select
        }, status=201)


class SelectionRetrieveUpdateDestroyView(HTTPMethodView):
    async def get(self, request, subject, id):
        """
        선택지 디테일
        """
        query_selection = db_session.query(Selection). \
            filter(Question.subject == subject). \
            filter_by(id=id).one()
        if query_selection is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        return json({
            'question_subject': query_selection.question.subject,
            'id': query_selection.id,
            'select': query_selection.select
        }, status=200)

    async def delete(self, request, subject, id):
        """
        선택지 삭제
        """
        query_selection = db_session.query(Selection). \
            filter(Question.subject == subject). \
            filter_by(id=id).one()
        if query_selection is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        db_session.delete(query_selection)
        db_session.commit()
        db_session.flush()
        db_session.close()

        return json(None, status=204)


blueprint.add_route(SelectionCreateListView.as_view(), '/survey/question/<subject>/selection', strict_slashes=True)
blueprint.add_route(SelectionRetrieveUpdateDestroyView.as_view(), '/survey/question/<subject>/selection/<id>',
                    strict_slashes=True)
