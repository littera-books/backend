import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE

from ..model import Product, Promotion

blueprint = Blueprint('Promotion')


@blueprint.route('/promotion', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    프로모션 리스트
    """
    return json(None, status=200)


@blueprint.route('/promotion', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    프로모션 생성
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    code_length = length_validation(data['code'], 20)
    if code_length is False:
        return json({'message': EXCEPTION_MESSAGE['invalid_description']}, status=400)

    try:
        promotion = Promotion(**data)
        db_session.add(promotion)
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({
            'message': error_message
        }, status=400)
    finally:
        db_session.close()

    query_promotion = query_validation(db_session, Promotion, code=data['code'])

    return json({
        'id': query_promotion.id,
        'code': query_promotion.code
    }, status=201)


@blueprint.route('/product/<product_id>/promotion', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, product_id):
    """
    프로모션 디테일
    """
    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    if query_product.promotion is None:
        return json({
            'id': 0,
            'code': ''
        }, status=200)

    return json({
        'id': query_product.promotion.id,
        'code': query_product.promotion.code
    }, status=200)


@blueprint.route('/product/<product_id>/promotion', methods=['PUT'], strict_slashes=True)
async def put(request, product_id):
    """
    프로모션 수정
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    if query_product.promotion is None:
        return json({
            'id': 0,
            'code': ''
        }, status=200)

    query_product.promotion.code = data['code']

    return json({
        'id': query_product.promotion.id,
        'code': query_product.promotion.code,
    }, status=200)


@blueprint.route('/product/<product_id>/promotion', methods=['DELETE'], strict_slashes=True)
async def delete(request, product_id):
    """
    프로모션 삭제
    """
    query_product = query_validation(db_session, Product, id=product_id)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    if query_product.promotion is None:
        return json({
            'id': 0,
            'code': ''
        }, status=200)

    db_session.delete(query_product.promotion)
    db_session.commit()
    db_session.close()

    return json(None, status=204)
