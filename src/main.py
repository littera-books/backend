from sanic import Sanic
from sanic.response import text

from common.database import Base, engine

from user.api import UserView

APP = Sanic(__name__)
APP.add_route(UserView.as_view(), '/user')


@APP.route('/')
async def main(request):
    """
    메인 entrypoint
    """
    return text('Welcome Littera API server')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)  # Base에 연결된 모든 테이블 매핑
    APP.run(host='localhost', port=8000)
