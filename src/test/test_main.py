import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from main import APP

def test_index_returns_200():
    request, response = APP.test_client.get('/')
    assert response.status == 200