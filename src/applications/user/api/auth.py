from sanic_jwt import exceptions

from common.database import db_session
from .. import EXCEPTION_MESSAGE
from ..model import User


async def authenticate(request, *args, **kwargs):
    """
    로그인 시 유저 정보가 담긴 JWT 를 전달해주는 메서드
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['empty_value'])

    user = db_session.query(User).filter_by(username=username).first()

    if user is None:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['none_user'])

    if password != user.password:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['invalid_password'])

    return user


async def payload_extender(payload, user):
    """
    JWT 의 payload 를 확장하는 함수
    """
    data = user.to_dict()
    payload.update(**data)

    return payload
