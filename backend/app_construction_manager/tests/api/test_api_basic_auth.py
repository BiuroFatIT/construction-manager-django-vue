import pytest

TEST_ORDER = 10

@pytest.mark.order(TEST_ORDER)
def test_authenticated_client_can_access_protected_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/')
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_login_with_invalid_credentials(unauthenticated_client, invalid_credentials):
    response = unauthenticated_client.post('/api/v1/auth/token/', data=invalid_credentials)
    assert response.status_code == 401