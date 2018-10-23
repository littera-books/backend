import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import empty_validation
from applications.admin.model import Admin
from .model import Message

blueprint = Blueprint('Message')


@blueprint.route('/message/<user_id>/count', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id):
    """
    메시지 갯수
    """
    try:
        query_message_count = db_session.query(Message). \
            filter_by(user_id=user_id).count()
    except sqlalchemy.exc.DataError:
        db_session.rollback()
        db_session.close()
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    return json({'count': query_message_count}, status=200)


@blueprint.route('/message/<user_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, user_id):
    return json(None, status=200)


@blueprint.route('/message/<user_id>', methods=['GET'], strict_slashes=True)
async def get(request, user_id):
    """
    메시지 리스트
    """
    page_args = request.args.get('page', None)
    if page_args is None:
        return json({'message': EXCEPTION_MESSAGE['invalid_page']}, status=400)

    page = int(page_args[0])
    if page is 0:
        return json({'message': EXCEPTION_MESSAGE['invalid_page']}, status=400)

    try:
        query_message = db_session.query(Message). \
            filter_by(user_id=user_id). \
            order_by(Message.created_at.desc()).\
            limit(5).offset((page - 1) * 5).all()
    except sqlalchemy.exc.DataError:
        db_session.rollback()
        db_session.close()
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    result = {
        'length': len(query_message),
        'items': []
    }

    for message in query_message:
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


@blueprint.route('/message/<user_id>/<message_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id, message_id):
    """
    메시지 디테일
    """
    try:
        query_message = db_session.query(Message). \
            filter_by(user_id=user_id). \
            filter_by(id=message_id).one()
    except sqlalchemy.exc.DataError:
        db_session.rollback()
        db_session.close()

    return json({
        'message_id': query_message.id,
        'body': query_message.body,
        'created_at': query_message.created_at,
    }, status=200)
