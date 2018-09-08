import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

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
    Base.metadata.create_all(bind=self.engine)

  def test_user_create(self):
    dummy_user = User(email='abc@abc.com', password='dummy')
    self.session.add(dummy_user)
    check_user = self.session.query(User).filter_by(email='abc@abc.com').first()
    assert dummy_user == check_user
    