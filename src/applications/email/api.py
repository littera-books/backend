import sqlalchemy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sanic import Blueprint, response
from sanic.response import json

from applications.email.methods import initial_smtp_instance, send_question_mail
from applications.user.model import User
from common.database import db_session
from common.messages import EXCEPTION_MESSAGE
from common.validation import empty_validation

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

    return response.redirect('https://www.littera.co.kr/login')


@blueprint.route('/send-email', methods=['OPTIONS'], strict_slashes=True)
async def options(request):
    return json(None, status=200)


@blueprint.route('/send-email', methods=['POST'], strict_slashes=True)
async def post(request):
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

    smtp = initial_smtp_instance()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        send_question_mail,
        args=[
            smtp,
            data['email'],
            data['name'],
            data['content'],
        ])
    scheduler.start()

    return json(None, status=200)
