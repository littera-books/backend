import os

import sqlalchemy
from sanic import Blueprint
from sanic.response import json

from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.read_secrets import ROOT_DIR
from common.random_seq import make_rand_seq
from common.validation import query_validation

from .model import Image

blueprint = Blueprint('Image')

STATIC_DIR = os.path.join(ROOT_DIR, 'static')


@blueprint.route('/image', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/image', methods=['POST'], strict_slashes=True)
async def post(request):
    """
    이미지 생성
    """
    name = request.form.get('name', None)
    raw_image = request.files.get('image', None)

    if (name and raw_image) is '' or (name and raw_image) is None:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    if not os.path.exists(STATIC_DIR):
        os.mkdir(STATIC_DIR, 0o0777)

    file, ext = os.path.splitext(raw_image.name)

    hashed_code = make_rand_seq()
    hashed_filename = file + '_' + hashed_code + ext

    with open(STATIC_DIR + '/' + hashed_filename, 'wb') as f:
        f.write(raw_image.body)

    try:
        image = Image()
        image.name = name
        image.image_url = '/static/' + hashed_filename
        db_session.add(image)
        db_session.commit()

    except sqlalchemy.exc.IntegrityError as e:
        error_message = e.orig.diag.message_detail
        db_session.rollback()
        return json({'message': error_message}, status=400)

    finally:
        db_session.close()

    return json({
        'name': name,
        'file': hashed_filename,
    }, status=201)


@blueprint.route('/image/<name>', methods=['OPTIONS'], strict_slashes=True)
async def options(request, name):
    return json({'name': name}, status=200)


@blueprint.route('/image/<name>', methods=['GET'], strict_slashes=True)
async def get(request, name):
    """
    이미지 디테일
    """
    query_image = query_validation(db_session, Image, name=name)
    if query_image is None:
        return json({'message': EXCEPTION_MESSAGE['none_image']}, status=400)

    return json({
        'id': query_image.id,
        'name': query_image.name,
        'url': query_image.image_url,
    }, status=200)
