from sanic_jwt import exceptions

from common.database import db_session
from user.model import User


async def authenticate(request, *args, **kwargs):
    """
    로그인 시 유저 정보가 담긴 JWT 를 전달해주는 메서드
    """
    data = request.json

    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed('아이디나 비밀번호를 입력해주세요')

    user = db_session.query(User).filter_by(username=username).first()

    if user is None:
        raise exceptions.AuthenticationFailed('유저 정보가 존재하지 않습니다')

    if password != user.password:
        raise exceptions.AuthenticationFailed('비밀번호가 일치하지 않습니다')

    return user


async def payload_extender(payload, user):
    """
    JWT 의 payload 를 확장하는 함수
    """
    data = user.to_dict()
    payload.update(**data)

    return payload
