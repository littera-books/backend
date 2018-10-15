import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.validation import empty_validation, query_validation, length_validation
from common.messages import EXCEPTION_MESSAGE

from ..model import Promotion

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


@blueprint.route('/promotion/<promotion_id>', methods=['OPTIONS', 'GET'], strict_slashes=True)
async def get(request, promotion_id):
    """
    프로모션 디테일
    """
    query_promotion = query_validation(db_session, Promotion, id=promotion_id)
    if query_promotion is None:
        return json({'message': EXCEPTION_MESSAGE['none_product']}, status=400)

    return json({
        'id': query_promotion.id,
        'code': query_promotion.code
    }, status=200)
