from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE

from .model import Product

blueprint = Blueprint('Product')


@blueprint.route('/product', methods=['OPTIONS', 'POST'], strict_slashes=True)
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

    product = Product(**data)
    db_session.add(product)
    db_session.commit()
    db_session.flush()
    db_session.close()

    query_product = query_validation(db_session, Product, months=data['months'])

    return json({
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description
    }, status=201)


@blueprint.route('/product/<months>', methods=['OPTIONS', 'DELETE'], strict_slashes=True)
async def delete(request, months):
    query_product = query_validation(db_session, Product, months=months)
    if query_product is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    db_session.delete(query_product)
    db_session.commit()
    db_session.flush()
    db_session.close()

    return json(None, status=204)
