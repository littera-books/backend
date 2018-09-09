from sanic import Sanic
from sanic.response import text

from common.database import Base, engine
from user.api import UserView

APP = Sanic(__name__)
APP.add_route(UserView.as_view(), '/user')


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