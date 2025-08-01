import pytest
from rest_framework import status

# Test order for company CRUD operations
TEST_ORDER = 2

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_create_company_missing_required_fields(api_client):
    response = api_client.post("/api/construction/manager/company/", data={}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'name' in response.data
    assert 'email' in response.data

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_get_nonexistent_company(api_client):
    response = api_client.get("/api/construction/manager/company/999999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_create_company_invalid_email(api_client, company_payload):
    payload = company_payload()
    payload['email'] = 'invalid-email-format'
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_delete_nonexistent_company(api_client):
    response = api_client.delete("/api/construction/manager/company/999999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_update_company_with_invalid_data(api_client, company_payload):
    # Create company first
    payload = company_payload()
    create_resp = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert create_resp.status_code == status.HTTP_201_CREATED
    company_id = create_resp.data['id']

    # Update with invalid email
    payload['email'] = 'not-an-email'
    update_resp = api_client.put(f"/api/construction/manager/company/{company_id}/", data=payload, format='json')
    assert update_resp.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in update_resp.data

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_partial_update_company(api_client, company_payload):
    payload = company_payload()
    create_resp = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert create_resp.status_code == status.HTTP_201_CREATED
    company_id = create_resp.data['id']

    patch_data = {'name': 'Updated Company Name'}
    patch_resp = api_client.patch(f"/api/construction/manager/company/{company_id}/", data=patch_data, format='json')
    assert patch_resp.status_code == status.HTTP_200_OK
    assert patch_resp.data['name'] == patch_data['name']

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_list_companies(api_client, company_payload):
    # Ensure at least one company exists
    payload = company_payload()
    api_client.post("/api/construction/manager/company/", data=payload, format='json')

    list_resp = api_client.get("/api/construction/manager/company/")
    assert list_resp.status_code == status.HTTP_200_OK
    assert isinstance(list_resp.data['results'], list)
    assert len(list_resp.data['results']) > 0