import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database import Base
from user.model import User


class TestDB(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        self.base = Base
        self.data = {
            'username': 'qwerty',
            'email': 'abc@abc.com',
            'phone': '01012345678',
            'password': 'dummy'}
        Base.metadata.create_all(bind=self.engine)

    def test_user_create(self):
        """
        DB에서 유저 생성 테스트
        """
        dummy_user = User(**self.data)
        self.session.add(dummy_user)

        query_user = self.session.query(User).filter_by(
            email=self.data['email']).first()
        self.assertEqual(dummy_user, query_user)

    def test_user_delete(self):
        """
        DB에서 유저 삭제 테스트
        """
        dummy_user = User(**self.data)
        self.session.add(dummy_user)

        query_user = self.session.query(User).filter_by(
            email=self.data['email']).first()
        self.session.delete(query_user)

        is_exists = self.session.query(User).filter_by(
            email=self.data['email']).count()
        self.assertEqual(is_exists, 0)
