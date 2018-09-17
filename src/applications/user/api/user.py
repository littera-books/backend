from sanic import Blueprint
from sanic.views import HTTPMethodView
from sanic.response import json

from common.database import db_session
from common.validation import Validation
from .. import SUCCEED_MESSAGE, EXCEPTION_MESSAGE
from ..model import User

blueprint = Blueprint('User')


class UserView(HTTPMethodView):
    """
    유저 관련 메서드 집합
    1. POST: 회원 가입
    2. PUT: 정보 수정
    3. PATCH: 비밀번호 수정
    4. DELETE: 회원 탈퇴
    """

    async def post(self, request):
        """
        회원 가입
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        phone_length = Validation.phone_validation(data['phone'])
        if phone_length is False:
            return json({'message': EXCEPTION_MESSAGE['invalid_phone']}, status=400)

        user = User(**data)
        db_session.add(user)
        db_session.commit()
        db_session.flush()
        db_session.close()

        query_user = Validation.none_validation(db_session, User, data['username'])

        return json({
            'username': query_user.username,
            'email': query_user.email,
            'phone': query_user.phone
        }, status=201)

    async def put(self, request):
        """
        회원 정보 수정
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        phone_length = Validation.phone_validation(data['phone'])
        if phone_length is False:
            return json({'message': EXCEPTION_MESSAGE['invalid_phone']}, status=400)

        query_user = Validation.none_validation(db_session, User, data['username'])
        if query_user is None:
            return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

        query_user.email = data['email']
        query_user.phone = data['phone']

        db_session.commit()
        db_session.flush()

        return json({
            'username': query_user.username,
            'email': query_user.email,
            'phone': query_user.phone
        }, status=200)

    async def patch(self, request):
        """
        비밀번호 수정
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        query_user = Validation.none_validation(db_session, User, data['username'])
        if query_user is None:
            return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

        query_user.password = data['password']

        db_session.commit()
        db_session.flush()

        return json({'message': SUCCEED_MESSAGE['patch_password']}, status=200)

    async def delete(self, request):
        """
        회원 탈퇴
        """
        data = request.json

        is_full = Validation.empty_validation(data)
        if is_full is False:
            return json({'message': EXCEPTION_MESSAGE['empty_value']}, status=400)

        query_user = Validation.none_validation(db_session, User, data['username'])
        if query_user is None:
            return json({'message': EXCEPTION_MESSAGE['none_user']}, status=400)

        if query_user.password != data['password']:
            return json({'message': EXCEPTION_MESSAGE['invalid_password']}, status=400)

        db_session.delete(query_user)
        db_session.commit()
        db_session.flush()
        db_session.close()

        return json(None, status=204)


blueprint.add_route(UserView.as_view(), '/user', strict_slashes=True)