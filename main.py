from sanic import Sanic
from sanic.response import text

APP = Sanic()


@APP.route('/')
async def main(request):
    """
    메인 entrypoint
    """
    return text('Welcome Littera API server')


if __name__ == '__main__':
    APP.run(host='localhost', port=8000)
