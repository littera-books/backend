import sqlalchemy
from sanic import Blueprint, response
from sanic.response import json

from applications.user.model import User
from common.database import db_session
from common.messages import EXCEPTION_MESSAGE

blueprint = Blueprint('Email')


@blueprint.route('/activate', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/activate', methods=['GET'], strict_slashes=True)
async def get(request):
    args = request.args
    email = args['email'][0]
    pk = args['pk'][0]

    query_user = db_session.query(User).filter_by(id=pk).filter_by(email=email).one()

    try:
        query_user.is_active = True
        db_session.commit()
    except sqlalchemy.exc.DataError:
        db_session.rollback()
        db_session.close()
        return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)
    finally:
        db_session.close()

    return response.redirect('http://localhost:3006/sign-in')
