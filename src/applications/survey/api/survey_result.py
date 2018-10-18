from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import query_validation
from common.messages import EXCEPTION_MESSAGE
from applications.user.model import User
from ..model import Selection, SurveyResult

blueprint = Blueprint('SurveyResult')


@blueprint.route('/survey/result/<user_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id):
    """
    설문 결과 호출
    """
    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    result = {
        'id': user_id,
        'length': len(query_user.survey_result),
        'items': []
    }

    for survey_result in query_user.survey_result:
        item = {
            'id': survey_result.selection.id,
            'select': survey_result.selection.select
        }

        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/survey/result/<user_id>', methods=['POST'], strict_slashes=True)
async def post(request, user_id):
    """
    설문 결과 생성
    """
    data = request.json
    selection_value_list = list(data.values())

    value_list = [i.split('-')[-1] for i in selection_value_list]

    for i in value_list:
        query_user = query_validation(db_session, User, id=user_id)
        if query_user is None:
            return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

        query_selection = query_validation(db_session, Selection, id=i)
        if query_selection is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        survey_result = SurveyResult()
        survey_result.user_id = query_user.id
        survey_result.selection_id = query_selection.id

        db_session.add(survey_result)
        db_session.commit()
        db_session.flush()
        db_session.close()

    result_user = query_validation(db_session, User, id=user_id)

    return json({
        'user': result_user.id,
    }, status=201)
