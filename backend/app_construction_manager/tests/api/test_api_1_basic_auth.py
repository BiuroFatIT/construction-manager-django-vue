import pytest

TEST_ORDER = 1

@pytest.mark.order(TEST_ORDER)
def test_authenticated_client_can_access_protected_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/')
    assert response.status_code == 200