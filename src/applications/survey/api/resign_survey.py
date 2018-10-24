import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import query_validation, empty_validation
from ..model import ResignSurvey

blueprint = Blueprint('ResignSurvey')


@blueprint.route('/survey/resign/count', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    탈퇴 설문 갯수
    """
    query_survey_count = db_session.query(ResignSurvey).count()

    return json({'count': query_survey_count}, status=200)


@blueprint.route('/survey/resign', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/survey/resign', methods=['GET'], strict_slashes=True)
async def get(request):
    """
    탈퇴 설문 리스트
    """
    page_args = request.args.get('page', None)
    if page_args is None:
        return json({'message': EXCEPTION_MESSAGE['invalid_page']}, status=400)

    page = int(page_args[0])
    if page is 0:
        return json({'message': EXCEPTION_MESSAGE['invalid_page']}, status=400)

    try:
        query_resign_survey = db_session.query(ResignSurvey). \
            order_by(ResignSurvey.created_at.desc()). \
            limit(5).offset((page - 1) * 5).all()
    except sqlalchemy.exc.DataError:
        db_session.rollback()
        db_session.close()
        return json({'message': EXCEPTION_MESSAGE['none_survey']}, status=400)

    result = {
        'length': len(query_resign_survey),
        'items': []
    }

    for survey in query_resign_survey:
        item = {
            'id': survey.id,
            'content': survey.content,
            'created_at': survey.created_at,
        }
        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/survey/resign', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    탈퇴 설문 생성
    """
    raw_data = request.form

    is_full = empty_validation(raw_data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    raw_content_value = raw_data['content'][0]
    result_data = {
        'content': raw_content_value
    }

    resign_survey = ResignSurvey(**result_data)
    db_session.add(resign_survey)
    db_session.commit()
    db_session.flush()

    query_resign_survey = query_validation(db_session, ResignSurvey, id=resign_survey.id)
    if query_resign_survey is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    return json({
        'id': query_resign_survey.id,
        'content': query_resign_survey.content
    }, status=201)


@blueprint.route('/survey/resign/<survey_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, survey_id):
    """
    탈퇴 질문 디테일
    """
    query_resign_survey = query_validation(db_session, ResignSurvey, id=survey_id)
    if query_resign_survey is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    return json({
        'id': query_resign_survey.id,
        'content': query_resign_survey.content,
        'created_at': query_resign_survey.created_at,
    }, status=200)


@blueprint.route('/survey/resign/<survey_id>', methods=['DELETE'], strict_slashes=True)
async def delete(request, survey_id):
    """
    탈퇴 질문 삭제
    """
    query_resign_survey = query_validation(db_session, ResignSurvey, id=survey_id)
    if query_resign_survey is None:
        return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

    db_session.delete(query_resign_survey)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)
