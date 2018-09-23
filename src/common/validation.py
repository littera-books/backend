def empty_validation(data):
    """
    세 가지 메서드에 대해 validation 수행
    :param data: request.json 값
    :return: 하나라도 blank('') 값이 들어오면 False, 아니면 True
    """
    data_set = tuple(data.values())

    return False if '' in data_set else True


def query_validation(session, model, **kwargs):
    """
    세 가지 메서드에 대해 validation 수행
    :param session: session 객체
    :param model: model 객체
    :param kwargs: 쿼리를 찾으려는 kwargs
    :return: 존재하면 User 객체, 없으면 None
    """
    return session.query(model).filter_by(**kwargs).first()


def phone_validation(phone):
    """
    핸드폰 길이 제한 11자 validation 수행
    :param phone: 입력값 phone_number
    :return: 통과 True, 불가 False
    """
    return True if len(phone) <= 11 else False
