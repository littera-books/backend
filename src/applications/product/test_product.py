import json
import unittest

from main import APP
from src.test.test_values import TestProductValues


class TestProductAPI(unittest.TestCase):
    """
    상품 관련 API 테스트
    """
    def tearDown(self):
        APP.test_client.delete(
            f'/product/{TestProductValues.default["months"]}'
        )

    def test_product_create_succeed(self):
        request, response = APP.test_client.post(
            '/product', data=json.dumps(TestProductValues.default)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('months'), TestProductValues.default['months'])
