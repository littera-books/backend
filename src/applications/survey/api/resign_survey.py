from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import query_validation, empty_validation
from ..model import ResignSurvey

blueprint = Blueprint('ResignSurvey')


@blueprint.route('/survey/resign', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    return json(None, status=200)


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
        'content': query_resign_survey.content
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