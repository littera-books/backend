from main import APP


def test_index_returns_200():
    request, response = APP.test_client.get('/')
    assert response.status == 200
