from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import query_validation
from applications.user.model import User
from ..model import Selection, SurveyResult

blueprint = Blueprint('SurveyResult')


@blueprint.route('/survey/result/<user_id>', methods=['OPTIONS', 'POST'], strict_slashes=True)
async def post(request, user_id):
    """
    설문 결과 생성
    """
    data = request.json
    selection_value_list = list(data.values())
    selection_value = ''.join(selection_value_list)
    split_value_list = selection_value.split('-')
    split_value = split_value_list[-1]

    query_user = query_validation(db_session, User, id=user_id)
    query_selection = query_validation(db_session, Selection, id=split_value)

    survey_result = SurveyResult()
    survey_result.user_id = query_user.id
    survey_result.selection_id = query_selection.id

    db_session.add(survey_result)
    db_session.commit()
    db_session.flush()
    db_session.close()

    query_result = query_validation(db_session, SurveyResult, selection_id=split_value)

    return json({
        'user': query_result.user.id,
        'selection': query_result.selection.select,
    }, status=201)
