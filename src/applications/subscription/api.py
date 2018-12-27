import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation
from common.messages import EXCEPTION_MESSAGE

from applications.user.model import User
from applications.product.model import Promotion
from .model import Subscription

blueprint = Blueprint('Subscription')


@blueprint.route('/subscription', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/subscription', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    일반 구독
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_user = query_validation(db_session, User, id=data['user_id'])
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    if query_user.subscription:
        return json({'message': EXCEPTION_MESSAGE['already_exist']}, status=400)

    try:
        subscription = Subscription(**data)
        db_session.add(subscription)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_subscription = query_validation(db_session, Subscription, user_id=data['user_id'])
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    return json({
        'user_id': query_subscription.user_id,
        'product_id': query_subscription.product.id
    }, status=201)


@blueprint.route('/subscription/promotion', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    return json(None, status=200)


@blueprint.route('/subscription/promotion', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    프로모션에 의한 구독
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_promotion = query_validation(db_session, Promotion, code=data['code'])
    if query_promotion is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    query_user = query_validation(db_session, User, id=data['user_id'])
    if query_user is None:
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

    if query_user.subscription:
        return json({'message': EXCEPTION_MESSAGE['already_exist']}, status=400)

    try:
        subscription = Subscription()
        subscription.user_id = data['user_id']
        subscription.product_id = query_promotion.product.id
        db_session.add(subscription)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_subscription = query_validation(db_session, Subscription, user_id=data['user_id'])
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    return json({
        'user_id': query_subscription.user_id,
        'product_id': query_subscription.product.id
    }, status=201)
