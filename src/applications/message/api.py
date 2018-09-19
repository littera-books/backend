from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

blueprint = Blueprint('Message')


class MessageView(HTTPMethodView):
    """
    메시지: 메시지 메서드 집합
    """

    async def get(self, request):
        return json({'message': 'message api'}, status=200)


blueprint.add_route(MessageView.as_view(), '/message', strict_slashes=True)
