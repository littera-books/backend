import json
import unittest

from main import APP
from src.test.test_values import TestProductValues


class TestProductAPI(unittest.TestCase):
    """
    상품 관련 API 테스트
    """
    def test_product_create_succeed(self):
        """
        상품 생성 테스트 성공
        """
        request, response = APP.test_client.post(
            '/product', data=json.dumps(TestProductValues.default)
        )
        self.assertEqual(response.status, 201)
        self.assertEqual(response.json.get('months'), TestProductValues.default['months'])
        self.product_id = response.json.get('id')

        request, response = APP.test_client.delete(
            f'/product/{self.product_id}'
        )
        self.assertEqual(response.status, 204)

    def test_product_get_list_succeed(self):
        """
        상품 리스트 보기 테스트 성공
        """
        request, response = APP.test_client.post(
            '/product', data=json.dumps(TestProductValues.default)
        )
        self.product_id = response.json.get('id')

        request, response = APP.test_client.get('/product?all=true')
        self.assertEqual(response.status, 200)

        request, response = APP.test_client.delete(
            f'/product/{self.product_id}'
        )
        self.assertEqual(response.status, 204)
