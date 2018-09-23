from sanic_jwt import exceptions

from common.database import db_session
from common.validation import empty_validation, query_validation
from common.messages import EXCEPTION_MESSAGE
from ..model import Admin


async def authenticate(request, *args, **kwargs):
    """
    로그인 시 유저 정보가 담긴 JWT 를 전달해주는 메서드
    """
    data = request.json

    is_full = empty_validation(data)
    if is_full is False:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['empty_value'])

    query_user = query_validation(db_session, Admin, username=data['username'])
    if query_user is None:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['none_user'])

    if query_user.password != data['password']:
        raise exceptions.AuthenticationFailed(EXCEPTION_MESSAGE['invalid_password'])

    return query_user


async def payload_extender(payload, user):
    """
    JWT 의 payload 를 확장하는 함수
    """
    data = user.to_dict()
    payload.update(**data)

    return payload
