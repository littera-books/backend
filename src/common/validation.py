import sqlalchemy


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
    try:
        query_instance = session.query(model).filter_by(**kwargs).one()

    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        session.close()
        return None

    except sqlalchemy.orm.exc.NoResultFound:
        session.rollback()
        session.close()
        return None

    except sqlalchemy.exc.DataError:
        session.rollback()
        session.close()
        return None

    return query_instance


def length_validation(row, length):
    """
    각 테이블 row 길이 제한 validation 수행
    :param row: 입력하려는 row 값
    :param length: row 값이 제한하는 길이
    :return: 통과 True, 불가 False
    """
    return True if len(row) <= length else False
