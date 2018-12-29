from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation
from common.messages import EXCEPTION_MESSAGE

from applications.subscription.model import Subscription
from .model import Book

blueprint = Blueprint('Book')


@blueprint.route('/book/<subscription_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, subscription_id):
    return json(None, status=200)


@blueprint.route('/book/<subscription_id>', methods=['POST'], strict_slashes=True)
async def post(request, subscription_id):
    """
    도서 배송 정보 생성
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_subscription = query_validation(db_session, Subscription, id=subscription_id)
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    query_subscription.book.append(Book(**data))
    db_session.add(query_subscription)
    db_session.commit()
    db_session.flush()

    return json({
        'book_id': query_subscription.book[-1].id,
        'book_name': query_subscription.book[-1].name,
    }, status=201)


@blueprint.route('/book/<subscription_id>', methods=['GET'], strict_slashes=True)
async def get(request, subscription_id):
    """
    도서 리스트
    """
    query_subscription = query_validation(db_session, Subscription, id=subscription_id)
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    result = {
        'length': len(query_subscription.book),
        'months': query_subscription.product.months,
        'items': [],
    }

    for book in query_subscription.book:
        item = {
            'id': book.id,
            'order': book.order,
            'name': book.name,
            'created_at': book.created_at,
        }

        result['items'].append(item)

    result['items'] = sorted(result['items'], key=lambda x: x['id'])

    return json(result, status=200)


@blueprint.route('/book/<subscription_id>/<book_id>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, subscription_id, book_id):
    return json(None, status=200)


@blueprint.route('/book/<subscription_id>/<book_id>', methods=['GET'], strict_slashes=True)
async def get(request, subscription_id, book_id):
    """
    도서 디테일
    """
    query_subscription = query_validation(db_session, Subscription, id=subscription_id)
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    query_book = query_validation(db_session, Book, id=book_id)
    if query_book is None:
        return json({'message': EXCEPTION_MESSAGE['none_book']}, status=400)

    return json({
        'id': query_book.id,
        'order': query_book.order,
        'name': query_book.name,
        'created_at': query_book.created_at,
        'months': query_subscription.product.months,
    }, status=200)


@blueprint.route('/book/<subscription_id>/<book_id>', methods=['PUT'], strict_slashes=True)
async def put(request, subscription_id, book_id):
    """
    도서 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_subscription = query_validation(db_session, Subscription, id=subscription_id)
    if query_subscription is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    query_book = query_validation(db_session, Book, id=book_id)
    if query_book is None:
        return json({'message': EXCEPTION_MESSAGE['none_book']}, status=400)

    query_book.order = data['order']
    query_book.name = data['name']
    db_session.commit()
    db_session.flush()

    return json({
        'id': query_book.id,
        'order': query_book.order,
        'name': query_book.name,
        'created_at': query_book.created_at,
        'months': query_subscription.product.months,
    }, status=200)


@blueprint.route('/book/<subscription_id>/<book_id>', methods=['DELETE'], strict_slashes=True)
async def delete(request, subscription_id, book_id):
    """
    도서 삭제
    """
    query_book = query_validation(db_session, Book, id=book_id)
    if query_book is None:
        return json({'message': EXCEPTION_MESSAGE['none_book']}, status=400)

    db_session.delete(query_book)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)
