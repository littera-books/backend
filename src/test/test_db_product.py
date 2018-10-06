import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.database import Base
from common.validation import query_validation
from applications.product.model import Product
from .test_values import TestProductValues


class TestDBProduct(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:', echo=True)
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        self.base = Base
        Base.metadata.create_all(bind=self.engine)

    def test_product_create_succeed(self):
        """
        상품 생성 테스트 성공
        """
        dummy_product = Product(**TestProductValues.default)
        self.session.add(dummy_product)
        self.session.commit()

        query_product = query_validation(self.session, Product, months=TestProductValues.default['months'])
        self.assertEqual(query_product.price, TestProductValues.default['price'])
