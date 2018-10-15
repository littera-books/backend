from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Question, Selection

blueprint = Blueprint('SurveySelection')


@blueprint.route('/survey/question/<question_id>/selection', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, question_id):
    """
    선택지 호출
    """
    query_question = query_validation(db_session, Question, id=question_id)
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


@blueprint.route('/survey/question/<question_id>/selection', methods=['POST'], strict_slashes=True)
async def post(request, question_id):
    """
    선택지 생성
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_question = query_validation(db_session, Question, id=question_id)
    if query_question is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    query_question.selection.append(Selection(**data))
    db_session.add(query_question)
    db_session.commit()
    db_session.flush()

    return json({
        'question_id': query_question.id,
        'id': query_question.selection[-1].id,
        'select': query_question.selection[-1].select
    }, status=201)


@blueprint.route('/survey/question/<question_id>/selection/<id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, question_id, id):
    """
    선택지 디테일
    """
    query_selection = db_session.query(Selection). \
        filter(Question.id == question_id). \
        filter_by(id=id).one()
    if query_selection is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    return json({
        'question_id': query_selection.question.id,
        'id': query_selection.id,
        'select': query_selection.select
    }, status=200)


@blueprint.route('/survey/question/<question_id>/selection/<id>', methods=['PUT'], strict_slashes=True)
async def put(request, question_id, id):
    """
    선택지 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_selection = db_session.query(Selection). \
        filter(Question.id == question_id). \
        filter_by(id=id).one()
    if query_selection is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    query_selection.select = data['select']
    db_session.commit()
    db_session.flush()

    return json({
        'question_id': query_selection.question.id,
        'id': query_selection.id,
        'select': query_selection.select
    }, status=200)


@blueprint.route('/survey/question/<question_id>/selection/<id>', methods=['DELETE'], strict_slashes=True)
async def delete(request, question_id, id):
    """
    선택지 삭제
    """
    query_selection = db_session.query(Selection). \
        filter(Question.id == question_id). \
        filter_by(id=id).one()
    if query_selection is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    db_session.delete(query_selection)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)
