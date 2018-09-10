from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from user.model import User


class UserView(HTTPMethodView):
    """
    유저 관련 메서드 집합
    1. POST: 회원 가입
    2. PATCH: 정보 수정
    3. DELETE: 회원 탈퇴
    """

    @staticmethod
    def empty_validation(data):
        """
        세 가지 메서드에 대해 validation 수행
        :param data: request.json 값
        :return: 하나라도 blank('') 값이 들어오면 False, 아니면 True
        """
        data_set = tuple(data.values())

        return False if '' in data_set else True

    async def post(self, request):
        """
        회원 가입
        """
        data = request.json
        is_empty = self.empty_validation(data)

        if is_empty is False:
            return json({'message': '정보를 모두 입력해주세요'}, status=400)

        user = User(**data)
        db_session.add(user)
        db_session.commit()
        db_session.flush()
        db_session.close()

        result = db_session.query(User).filter_by(username=data['username']).first()

        return json({
            'username': result.username,
            'email': result.email,
            'phone': result.phone,
            'password': result.password
        }, status=201)

    async def patch(self, request):
        """
        회원 정보 수정
        """
        data = request.json
        is_empty = self.empty_validation(data)

        if is_empty is False:
            return json({'message': '정보를 모두 입력해주세요'}, status=400)

        user = db_session.query(User).filter_by(username=data['username']).first()

        user.email = data['email']
        user.phone = data['phone']
        user.password = data['password']

        db_session.commit()
        db_session.flush()

        return json({
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'password': user.password
        }, status=200)

    async def delete(self, request):
        """
        회원 탈퇴
        """
        data = request.json
        is_empty = self.empty_validation(data)

        if is_empty is False:
            return json({'message': '정보를 모두 입력해주세요'}, status=400)

        user = db_session.query(User).filter_by(username=data['username']).first()

        if user.password == data['password']:
            db_session.delete(user)
            db_session.commit()
            db_session.flush()
            db_session.close()
            return json(None, status=204)

        return json({'message': '유저 정보가 맞지 않습니다.'}, status=400)
