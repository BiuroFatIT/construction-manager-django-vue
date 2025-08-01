import pytest

TEST_ORDER = 1

@pytest.mark.order(TEST_ORDER)
def test_client_can_access_company_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/company/')
    assert response.status_code == 200

@pytest.mark.order(TEST_ORDER)
def test_client_can_access_products_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/products/')
    assert response.status_code == 200