class TestAdminValues:
    """
    관리자 테스트용 더미 값들
    """
    default = {
        'username': 'admin',
        'password': 'super'
    }
    patch = {
        'username': 'admin',
        'password': 'abcd'
    }
    empty = {
        'username': '',
        'password': ''
    }
    invalid_password = {
        'username': 'admin',
        'password': '4321'
    }
    none = {
        'username': 'coffee',
        'password': 'super'
    }


class TestUserValues:
    """
    유저 테스트용 더미 값들
    """
    default = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'address': '서울시 행복구 희망동',
        'email': 'dummy@test.com',
        'phone': '01012345678',
        'password': '1234'
    }
    put = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'address': '서울시 별빛구 달빛동',
        'email': 'chubby@test.com',
        'phone': '01098765432'
    }
    patch = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'password': 'abcd'
    }
    empty = {
        'last_name': '',
        'first_name': '',
        'address': '',
        'email': '',
        'phone': '',
        'password': ''
    }
    invalid_password = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'address': '서울시 행복구 희망동',
        'email': 'dummy@test.com',
        'phone': '01012345678',
        'password': '4321'
    }
    invalid_phone = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'address': '서울시 행복구 희망동',
        'email': 'dummy@test.com',
        'phone': '0101234567801012345678',
        'password': '1234'
    }
    none = {
        'last_name': 'hummy',
        'first_name': 'dummy',
        'address': '서울시 행복구 희망동',
        'email': 'none_email@test.com',
        'phone': '01012345678',
        'password': '1234'
    }


class TestQuestionValues:
    default = {
        'subject': 'dummy',
        'title': '테스트 질문'
    }
    put = {
        'subject': 'dummy',
        'title': '안녕하세요'
    }
    empty = {
        'subject': '',
        'title': ''
    }
    none = {
        'subject': 'coffee',
        'title': '테스트 질문'
    }


class TestSelectionValues:
    default = {
        'select': '테스트 선택지',
        'is_accepted': True,
    }


class TestProductValues:
    default = {
        'months': 30,
        'price': 990000,
        'description': '30개월 구독권'
    }


class TestResignSurveyValues:
    default = {
        'content': '별로에요',
    }
