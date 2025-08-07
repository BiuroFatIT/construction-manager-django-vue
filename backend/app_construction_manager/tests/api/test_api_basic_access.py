import pytest
from rest_framework import status

TEST_ORDER = 11

@pytest.mark.order(TEST_ORDER)
def test_client_can_access_products_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/products/')
    assert response.status_code == 200

@pytest.mark.order(TEST_ORDER)
def test_client_can_access_user_endpoint(api_client, db):
    response = api_client.get('/api/construction/manager/user/')
    assert response.status_code == 200

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_list_companies(api_client, company_payload):
    # Ensure at least one company exists
    payload = company_payload()
    api_client.post("/api/construction/manager/company/", data=payload, format='json')

    list_resp = api_client.get("/api/construction/manager/company/?page=1&page_size=20")
    assert list_resp.status_code == status.HTTP_200_OK
    assert isinstance(list_resp.data["results"], list)
    assert len(list_resp.data["results"]) > 0
