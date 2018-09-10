from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from user.model import User


class AuthView(HTTPMethodView):
    """
    인증 관련 메서드 집합
    1. POST: 로그인
    """

    async def post(self, request):
        """
        로그인
        """
        data = request.json

        user = db_session.query(User).filter_by(username=data['username']).first()

        if user.password == data['password']:
            return json({'message': 'ok'}, status=200)

        return json({'message': '유저 정보가 맞지 않습니다.'}, status=401)
