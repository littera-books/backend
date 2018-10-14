import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Question

blueprint = Blueprint('SurveyQuestion')


@blueprint.route('/survey/question', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
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


@blueprint.route('/survey/questions', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    질문 및 선택지 리스트 반환
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
            'title': question.title,
            'selection_items': [],
        }

        for selection in question.selection:
            selection_item = {
                'id': selection.id,
                'select': selection.select,
            }
            item['selection_items'].append(selection_item)

        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/survey/question', methods=['POST'], strict_slashes=True)
async def post(request):
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

    try:
        question = Question(**data)
        db_session.add(question)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_question = query_validation(db_session, Question, subject=data['subject'])

    return json({
        'subject': query_question.subject,
        'title': query_question.title
    }, status=201)


@blueprint.route('/survey/question/<subject>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, subject):
    """
    질문 디테일
    """

    query_question = query_validation(db_session, Question, subject=subject)
    if query_question is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    return json({
        'subject': query_question.subject,
        'title': query_question.title
    }, status=200)


@blueprint.route('/survey/question/<subject>', methods=['PUT'], strict_slashes=True)
async def put(request, subject):
    """
    질문 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    subject_length = length_validation(data['subject'], 50)
    if subject_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_subject']}, status=400)

    query_question = query_validation(db_session, Question, subject=subject)
    if query_question is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    try:
        query_question.title = data['title']
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        db_session.close()
        return json({
            'message': error_message
        }, status=400)

    return json({
        'subject': query_question.subject,
        'title': query_question.title
    }, status=200)


@blueprint.route('/survey/question/<subject>', methods=['DELETE'], strict_slashes=True)
async def delete(request, subject):
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
