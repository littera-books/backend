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
    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        db_session.close()
        return json({
            'message': error_message
        }, status=400)

    return json({
        'id': promotion.id,
        'code': promotion.code
    }, status=200)
