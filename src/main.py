import os

from sanic import Sanic
from sanic.response import text
from sanic_cors import CORS
from sanic_jwt import Initialize

from common.database import Base, engine
from common.read_secrets import ROOT_DIR
from applications.user.api import auth as auth_user, user
from applications.admin.api import auth as auth_admin, admin
from applications.survey.api import question, selection, survey_result, resign_survey
from applications.accept import api as accept_api
from applications.message import api as message_api
from applications.product.api import product, promotion
from applications.subscription import api as subscription_api
from applications.email import api as email_api
from applications.content import api as image_api
from applications.book import api as book_api

STATIC_DIR = os.path.join(ROOT_DIR, 'static')

APP = Sanic(__name__)
APP.static('/static', STATIC_DIR)
CORS(APP, resources={r'/*': {'origins': ['https://admin.littera.co.kr',
                                         'https://www.littera.co.kr',
                                         'http://localhost:3000',
                                         'http://localhost:3006',
                                         ]}})

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
APP.blueprint(product.blueprint)
APP.blueprint(promotion.blueprint)
APP.blueprint(accept_api.blueprint)
APP.blueprint(message_api.blueprint)
APP.blueprint(subscription_api.blueprint)
APP.blueprint(email_api.blueprint)
APP.blueprint(image_api.blueprint)
APP.blueprint(book_api.blueprint)


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


# ssl = {
#     'cert': '/app/archive/www.littera.co.kr/cert1.pem',
#     'key': '/app/archive/www.littera.co.kr/privkey1.pem',
# }

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000)
