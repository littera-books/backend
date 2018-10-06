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
        'username': 'dummy',
        'email': 'dummy@test.com',
        'phone': '01012345678',
        'password': '1234'
    }
    put = {
        'username': 'dummy',
        'email': 'chubby@test.com',
        'phone': '01098765432'
    }
    patch = {
        'username': 'dummy',
        'password': 'abcd'
    }
    empty = {
        'username': '',
        'email': '',
        'phone': '',
        'password': ''
    }
    invalid_password = {
        'username': 'dummy',
        'email': 'dummy@test.com',
        'phone': '01012345678',
        'password': '4321'
    }
    invalid_phone = {
        'username': 'dummy',
        'email': 'dummy@test.com',
        'phone': '010123456789',
        'password': '1234'
    }
    none = {
        'username': 'coffee',
        'email': 'dummy@test.com',
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
        'select': '테스트 선택지'
    }


class TestProductValues:
    default = {
        'months': 30,
        'price': 990000,
        'description': '30개월 구독권'
    }
