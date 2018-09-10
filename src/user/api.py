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
        data = request.json

        user = User(**data)
        db_session.add(user)
        db_session.commit()
        db_session.flush()

        result = db_session.query(User).filter_by(username=data['username']).first()

        return json({
            'username': result.username,
            'email': result.email,
            'password': result.password
        }, status=201)

    async def delete(self, request):
        """
        회원 탈퇴
        """
        data = request.json

        user = db_session.query(User).filter_by(username=data['username']).first()

        if user.password == data['password']:
            db_session.delete(user)
            db_session.commit()
            db_session.flush()
            return json(None, status=204)

        return json({'message': '유저 정보가 맞지 않습니다.'}, status=400)
