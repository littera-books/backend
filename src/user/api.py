from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session

from .model import User


class UserView(HTTPMethodView):
    """
    유저 관련 메서드 집합
    """

    async def post(self, request):
        """
        회원 가입
        """
        email = request.json['email']
        password = request.json['password']

        user = User(email=email, password=password)
        db_session.add(user)
        db_session.commit()
        db_session.flush()
        result = db_session.query(User).filter_by(email=email).first()

        return json({'email': result.email, 'password': result.password})
