from sanic import Sanic
from sanic.response import text
from sanic_cors import CORS
from sanic_jwt import Initialize

from common.database import Base, engine
from applications.user.api import auth as auth_user, user
from applications.admin.api import auth as auth_admin, admin
from applications.survey.api import question, selection, survey_result, resign_survey
from applications.message import api as message_api
from applications.product import api as product_api

APP = Sanic(__name__)
CORS(APP, resources={r'/*': {'origins': ['http://localhost:3000', 'http://localhost:3006']}})

Initialize(instance=user.blueprint,
           app=APP,
           authenticate=auth_user.authenticate,
           extend_payload=auth_user.payload_extender,
           access_token_name='user_token',
           url_prefix='/auth/user')
Initialize(instance=admin.blueprint,
           app=APP,
           authenticate=auth_admin.authenticate,
           extend_payload=auth_admin.payload_extender,
           access_token_name='admin_token',
           url_prefix='/auth/admin')

APP.blueprint(user.blueprint)
APP.blueprint(admin.blueprint)
APP.blueprint(question.blueprint)
APP.blueprint(selection.blueprint)
APP.blueprint(survey_result.blueprint)
APP.blueprint(resign_survey.blueprint)
APP.blueprint(message_api.blueprint)
APP.blueprint(product_api.blueprint)


@APP.listener('before_server_start')
async def setup_db(app, loop):
    # Base에 연결된 모든 테이블 매핑
    Base.metadata.create_all(bind=engine)


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    print('\nWelcome Littera API server\n')


@APP.route('/')
async def main(request):
    """
    메인 entrypoint
    """
    return text('Welcome Littera API server')


if __name__ == '__main__':
    APP.run(host='localhost', port=8000)
