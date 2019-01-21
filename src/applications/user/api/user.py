import sqlalchemy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sanic import Blueprint
from sanic.response import json

from applications.email.methods import initial_smtp_instance, send_activate_mail, send_reset_password_mail
from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import SUCCEED_MESSAGE, EXCEPTION_MESSAGE
from common.random_seq import make_rand_seq
from ..model import User

blueprint = Blueprint('User')


@blueprint.route('/user', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    회원 리스트
    """
    query_user = db_session.query(User).order_by(User.created_at).all()

    result = {
        'length': len(query_user),
        'items': []
    }

    for user in query_user:
        item = {
            'id': user.id,
            'email': user.email,
            'is_active': user.is_active,
        }
        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/user', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    회원 가입
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    try:
        user = User(**data)
        db_session.add(user)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_user = query_validation(db_session, User, email=data['email'])

    smtp = initial_smtp_instance()
    scheduler = AsyncIOScheduler()
    pick_user_id = str(query_user.id)
    scheduler.add_job(send_activate_mail,
                      args=[smtp,
                            query_user.email,
                            pick_user_id,
                            request.scheme,
                            request.host])
    scheduler.start()

    return json({
        'id': query_user.id,
        'email': query_user.email,
    }, status=201)


@blueprint.route('/user/toggle-active/<user_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, user_id):
    return json(None, status=200)


@blueprint.route('/user/toggle-active/<user_id>', methods=['PATCH'], strict_slashes=True)
async def patch(request, user_id):
    """
    회원 활성화 토글
    """
    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    if query_user.is_active is False:
        query_user.is_active = True
    else:
        query_user.is_active = False

    db_session.commit()
    db_session.flush()
    db_session.close()

    return json({'message': SUCCEED_MESSAGE['patch_active']}, status=200)


@blueprint.route('/user/<user_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, user_id):
    """
    회원 정보 호출
    """
    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    return json({
        'id': query_user.id,
        'first_name': query_user.first_name,
        'last_name': query_user.last_name,
        'address': query_user.address,
        'extra_address': query_user.extra_address,
        'phone': query_user.phone,
        'email': query_user.email,
        'created_at': query_user.created_at,
        'is_active': query_user.is_active,
        'has_survey': True if len(query_user.survey_result) > 0 else False,
    }, status=200)


@blueprint.route('/user/<user_id>', methods=['PUT'], strict_slashes=True)
async def put(request, user_id):
    """
    회원 정보 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    first_name_length = length_validation(data['first_name'], 20)
    if first_name_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_username']}, status=400)

    last_name_length = length_validation(data['last_name'], 20)
    if last_name_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_username']}, status=400)

    phone_length = length_validation(data['phone'], 20)
    if phone_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_phone']}, status=400)

    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    try:
        query_user.first_name = data['first_name']
        query_user.last_name = data['last_name']
        query_user.address = data['address']
        query_user.extra_address = data['extra_address']
        query_user.phone = data['phone']
        if data.get('email'):
            query_user.email = data['email']
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        db_session.close()
        return json({
            'message': error_message
        }, status=400)

    return json({
        'id': query_user.id,
        'email': query_user.email,
    }, status=200)


@blueprint.route('/user/<user_id>', methods=['PATCH'], strict_slashes=True)
async def patch(request, user_id):
    """
    비밀번호 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    query_user.password = data['password']

    db_session.commit()
    db_session.flush()
    db_session.close()

    return json({'message': SUCCEED_MESSAGE['patch_password']}, status=200)


@blueprint.route('/user/<user_id>', methods=['DELETE'], strict_slashes=True)
async def delete(request, user_id):
    """
    회원 탈퇴
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_user = query_validation(db_session, User, id=user_id)
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    if query_user.password != data['password']:
        return json({'message': EXCEPTION_MESSAGE['invalid_password']}, status=400)

    for subscription in query_user.subscription:
        db_session.delete(subscription)
        db_session.commit()

    db_session.delete(query_user)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)


@blueprint.route('/user/reset-password', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/user/reset-password', methods=['POST'], strict_slashes=True)
async def post(request):
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_user = query_validation(db_session, User, email=data['email'])
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    new_password = make_rand_seq()

    query_user.password = new_password

    db_session.commit()
    db_session.close()

    smtp = initial_smtp_instance()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_reset_password_mail,
        args=[smtp,
              data['email'],
              new_password,
              ]
    )
    scheduler.start()

    return json(None, status=200)
