import os

import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.random_seq import make_rand_seq
from common.read_secrets import ROOT_DIR
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE

from ..model import Product

blueprint = Blueprint('Product')

STATIC_DIR = os.path.join(ROOT_DIR, 'static')


@blueprint.route('/product', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request):
    """
    상품 리스트 보기
    """
    args = request.args
    if args:
        query_product = db_session.query(Product).order_by(Product.created_at).all()
    else:
        query_product = db_session.query(Product).filter_by(is_visible=True).order_by(Product.created_at).all()

    result = {
        'length': len(query_product),
        'items': []
    }

    for product in query_product:
        item = {
            'id': product.id,
            'books': product.books,
            'months': product.months,
            'price': product.price,
            'description': product.description,
            'url': product.thumbnail_url,
            'is_visible': product.is_visible,
        }
        result['items'].append(item)

    return json(result, status=200)


@blueprint.route('/product', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    상품 생성
    """
    books = request.form.get('books', None)
    months = request.form.get('months', None)
    price = request.form.get('price', None)
    description = request.form.get('description', None)
    raw_thumbnail = request.files.get('thumbnail', None)

    if not os.path.exists(STATIC_DIR):
        os.mkdir(STATIC_DIR, 0o0777)

    file, ext = os.path.splitext(raw_thumbnail.name)

    hashed_code = make_rand_seq()
    hashed_filename = file + '_' + hashed_code + ext

    with open(STATIC_DIR + '/' + hashed_filename, 'wb') as f:
        f.write(raw_thumbnail.body)

    data = {
        'books': books,
        'months': months,
        'price': price,
        'description': description,
        'thumbnail_url': '/static/' + hashed_filename,
    }

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
        'books': query_product.books,
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description,
        'url': query_product.thumbnail_url,
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
        'books': query_product.books,
        'months': query_product.months,
        'price': query_product.price,
        'description': query_product.description,
        'is_visible': query_product.is_visible,
        'url': query_product.thumbnail_url,
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
        query_product.books = data['books']
        query_product.price = data['price']
        query_product.description = data['description']
        query_product.is_visible = data['is_visible']
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
        'books': query_product.books,
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
