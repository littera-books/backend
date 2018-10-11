from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import empty_validation, query_validation
from applications.user.model import User
from applications.admin.model import Admin
from .model import Message

blueprint = Blueprint('Message')


@blueprint.route('/message/<user_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id):
    """
    메시지 리스트
    """
    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    result = {
        'length': len(query_user.admin),
        'items': []
    }

    for message in query_user.admin:
        item = {
            'id': message.id,
            'body': message.body,
            'created_at': message.created_at,
        }

        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/message/<user_id>', methods=['POST'], strict_slashes=True)
async def post(request, user_id):
    """
    메시지 생성
    """
    raw_data = request.form

    is_full = empty_validation(raw_data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    raw_content_value = raw_data['content'][0]

    query_admin = db_session.query(Admin).first()

    message = Message()
    message.body = raw_content_value
    message.user_id = user_id
    message.admin_id = query_admin.id

    db_session.add(message)
    db_session.commit()
    db_session.flush()

    return json({
        'user_id': message.user_id
    }, status=201)
