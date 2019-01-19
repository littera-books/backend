import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation
from common.messages import EXCEPTION_MESSAGE

from applications.user.model import User
from applications.product.model import Promotion, Product
from .model import Subscription

blueprint = Blueprint('Subscription')


@blueprint.route('/subscription/<user_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, user_id):
    return json(None, status=200)


@blueprint.route('/subscription/<user_id>', methods=['GET'], strict_slashes=True)
async def get(request, user_id):
    """
    구독 리스트
    """
    query_subscription = db_session.query(Subscription).filter_by(user_id=user_id).order_by(
        Subscription.created_at).all()

    result = {
        'length': len(query_subscription),
        'items': [],
    }

    for subscription in query_subscription:
        item = {
            'id': subscription.id,
            'first_name': subscription.first_name,
            'last_name': subscription.last_name,
            'address': subscription.address,
            'extra_address': subscription.extra_address,
            'phone': subscription.phone,
            'created_at': subscription.created_at,
        }

        product = query_validation(db_session, Product, id=subscription.product_id)
        if product is None:
            item['product'] = {}
        item['product'] = {
            'id': product.id,
            'books': product.books,
            'months': product.months,
            'price': product.price,
            'discount_amount': product.discount_amount,
        }

        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/subscription/<user_id>/<subscription_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, user_id, subscription_id):
    return json(None, status=200)


@blueprint.route('/subscription/<user_id>/<subscription_id>', methods=['GET'], strict_slashes=True)
async def get(request, user_id, subscription_id):
    """
    구독 디테일
    """
    query_subscription = query_validation(db_session, Subscription, id=subscription_id)
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    result = {
        'id': query_subscription.id,
        'first_name': query_subscription.first_name,
        'last_name': query_subscription.last_name,
        'address': query_subscription.address,
        'extra_address': query_subscription.extra_address,
        'phone': query_subscription.phone,
        'created_at': query_subscription.created_at,
    }

    product = query_validation(db_session, Product, id=query_subscription.product_id)
    if product is None:
        result['product'] = {}
    result['product'] = {
        'id': product.id,
        'books': product.books,
        'months': product.months,
        'price': product.price,
        'discount_amount': product.discount_amount,
    }

    return json(result, status=200)


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

    try:
        subscription = Subscription(**data)
        db_session.add(subscription)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        db_session.close()
        return json({
            'message': error_message
        }, status=400)

    return json({
        'user_id': subscription.user_id,
        'product_id': subscription.product.id
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

    return json({
        'user_id': subscription.user_id,
        'product_id': subscription.product.id
    }, status=201)
