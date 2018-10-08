import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database import Base
from common.validation import query_validation
from applications.user.model import User
from applications.admin.model import Admin
from .test_values import TestAdminValues, TestUserValues


class TestDBUserAdmin(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        self.base = Base
        Base.metadata.create_all(bind=self.engine)

    def test_user_create(self):
        """
        DB에서 유저 생성 테스트
        """
        dummy_user = User(**TestUserValues.default)
        self.session.add(dummy_user)

        query_user = query_validation(self.session, User, email=TestUserValues.default['email'])
        self.assertEqual(dummy_user, query_user)

    def test_user_patch(self):
        """
        DB에서 유저 정보 수정 테스트
        """
        dummy_user = User(**TestUserValues.default)
        self.session.add(dummy_user)

        query_user = query_validation(self.session, User, email=TestUserValues.default['email'])

        query_user.email = TestUserValues.put['email']
        query_user.phone = TestUserValues.put['phone']
        query_user.password = TestUserValues.patch['password']

        self.assertNotEqual(query_user.email, TestUserValues.default['email'])
        self.assertNotEqual(query_user.phone, TestUserValues.default['phone'])
        self.assertNotEqual(query_user.password, TestUserValues.default['password'])

    def test_user_delete(self):
        """
        DB에서 유저 삭제 테스트
        """
        dummy_user = User(**TestUserValues.default)
        self.session.add(dummy_user)

        query_user = query_validation(self.session, User, email=TestUserValues.default['email'])
        self.session.delete(query_user)

        is_exists = self.session.query(User).filter_by(
            email=TestUserValues.default['email']).count()
        self.assertEqual(is_exists, 0)

    #     관리자 테스트     #

    def test_admin_create(self):
        """
        DB에서 관리자 생성 테스트
        """
        dummy_admin = Admin(**TestAdminValues.default)
        self.session.add(dummy_admin)

        query_admin = query_validation(self.session, Admin, username=TestAdminValues.default['username'])
        self.assertEqual(dummy_admin, query_admin)

    def test_admin_patch(self):
        """
        DB에서 관리자 비밀번호 수정 테스트
        """
        dummy_admin = Admin(**TestAdminValues.default)
        self.session.add(dummy_admin)

        query_admin = query_validation(self.session, Admin, username=TestAdminValues.default['username'])

        query_admin.password = TestAdminValues.patch['password']
        self.assertNotEqual(query_admin.password, TestAdminValues.default['password'])

    def test_admin_delete(self):
        """
        DB에서 관리자 삭제 테스트
        """
        dummy_admin = Admin(**TestAdminValues.default)
        self.session.add(dummy_admin)

        query_admin = query_validation(self.session, Admin, username=TestAdminValues.default['username'])
        self.session.delete(query_admin)

        is_exists = self.session.query(Admin).filter_by(
            username=TestAdminValues.default['username']).count()
        self.assertEqual(is_exists, 0)
