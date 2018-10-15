from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import query_validation
from applications.user.model import User
from applications.survey.model import Selection

blueprint = Blueprint('Accept')


@blueprint.route('/accept/<user_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id):
    return json({
        'user': user_id,
    }, status=200)


@blueprint.route('/accept/<user_id>', methods=['POST'], strict_slashes=True)
async def post(request, user_id):
    """
    승인 / 거절 여부 판단
    """
    data = request.json
    selection_value_list = list(data.values())

    value_list = [i.split('-')[-1] for i in selection_value_list]

    denied_count = 0

    for i in value_list:
        query_user = query_validation(db_session, User, id=user_id)
        if query_user is None:
            return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

        query_selection = query_validation(db_session, Selection, id=i)
        if query_selection is None:
            return json({'message': EXCEPTION_MESSAGE['none_question']}, status=400)

        if query_selection.is_accepted is False:
            denied_count = denied_count + 1

    if denied_count > 0:
        return json({'message': False}, status=400)
    return json({'message': True}, status=200)
