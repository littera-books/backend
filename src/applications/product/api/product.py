import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE

from ..model import Product

blueprint = Blueprint('Product')


@blueprint.route('/product', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    상품 리스트 보기
    """
    query_product = db_session.query(Product).order_by(Product.created_at).all()

    result = {
        'length': len(query_product),
        'items': []
    }

    for product in query_product:
        item = {
            'id': product.id,
            'months': product.months,
            'price': product.price,
            'description': product.description
        }
        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/product', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    상품 생성
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    description_length = length_validation(data['description'], 100)
    if description_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_description']}, status=400)

    try:
        product = Product(**data)
        db_session.add(product)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_product = query_validation(db_session, Product, months=data['months'])

    return json({
        'id': query_product.id,
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description
    }, status=201)


@blueprint.route('/product/<product_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, product_id):
    """
    상품 디테일
    """
    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    return json({
        'id': query_product.id,
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description,
    }, status=200)


@blueprint.route('/product/<product_id>', methods=['PUT'], strict_slashes=True)
async def put(request, product_id):
    """
    상품 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    try:
        query_product.months = data['months']
        query_product.price = data['price']
        query_product.description = data['description']
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        db_session.close()
        return json({
            'message': error_message
        }, status=400)

    return json({
        'id': query_product.id,
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description,
    }, status=200)


@blueprint.route('/product/<product_id>', methods=['DELETE'], strict_slashes=True)
async def delete(request, product_id):
    """
    상품 삭제
    """
    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    db_session.delete(query_product)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)
