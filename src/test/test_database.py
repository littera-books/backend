import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database import Base
from applications.user.model import User
from applications.admin.model import Admin


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
        self.patch_data = {
            'email': 'dfg@dfg.com',
            'phone': '01098765432',
            'password': 'chubby'
        }
        self.admin_data = {
            'username': 'admin',
            'password': 'superuser'
        }
        self.admin_patch_data = {
            'password': 'supersuperuser'
        }
        Base.metadata.create_all(bind=self.engine)

    def test_user_create(self):
        """
        DB에서 유저 생성 테스트
        """
        dummy_user = User(**self.data)
        self.session.add(dummy_user)

        query_user = self.session.query(User).filter_by(
            username=self.data['username']).first()
        self.assertEqual(dummy_user, query_user)

    def test_user_patch(self):
        """
        DB에서 유저 정보 수정 테스트
        """
        dummy_user = User(**self.data)
        self.session.add(dummy_user)

        query_user = self.session.query(User).filter_by(
            username=self.data['username']).first()

        query_user.email = self.patch_data['email']
        query_user.phone = self.patch_data['phone']
        query_user.password = self.patch_data['password']

        self.assertNotEqual(query_user.email, self.data['email'])
        self.assertNotEqual(query_user.phone, self.data['phone'])
        self.assertNotEqual(query_user.password, self.data['password'])

    def test_user_delete(self):
        """
        DB에서 유저 삭제 테스트
        """
        dummy_user = User(**self.data)
        self.session.add(dummy_user)

        query_user = self.session.query(User).filter_by(
            username=self.data['username']).first()
        self.session.delete(query_user)

        is_exists = self.session.query(User).filter_by(
            username=self.data['username']).count()
        self.assertEqual(is_exists, 0)

    #     관리자 테스트     #

    def test_admin_create(self):
        """
        DB에서 관리자 생성 테스트
        """
        admin_user = Admin(**self.admin_data)
        self.session.add(admin_user)

        query_user = self.session.query(Admin).filter_by(
            username=self.admin_data['username']).first()
        self.assertEqual(admin_user, query_user)

    def test_admin_patch(self):
        """
        DB에서 관리자 비밀번호 수정 테스트
        """
        admin_user = Admin(**self.admin_data)
        self.session.add(admin_user)

        query_user = self.session.query(Admin).filter_by(
            username=self.admin_data['username']).first()

        query_user.password = self.admin_patch_data['password']

        self.assertNotEqual(query_user.password, self.admin_data['password'])
