import pytest
from app_construction_manager.models import Company, Address


# Test order for the company CRUD tests
TEST_ORDER = 20



@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_create_company(api_client, company_payload):
    payload = company_payload()
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}, response: {response.data}"
    assert response.data["name"] == payload["name"]
    assert response.data["address"]["street"] == payload["address"]["street"]  # Compare nested address data
    assert Company.objects.filter(name=payload["name"]).exists()

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_get_company(api_client, company_payload):
    company = Company.objects.create(**company_payload(as_instance=True))
    url = f"/api/construction/manager/company/{company.id}/"
    
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == company.name
    assert response.data["address"]["id"] == company.address.id  # Compare nested address ID

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_update_company(api_client, company_payload):
    company = Company.objects.create(**company_payload(as_instance=True))
    url = f"/api/construction/manager/company/{company.id}/"

    updated_data = company_payload()
    updated_data["name"] = "Updated Company Name"

    response = api_client.put(url, data=updated_data, format='json')
    assert response.status_code == 200
    assert response.data["name"] == "Updated Company Name"
    assert response.data["address"]["street"] == updated_data["address"]["street"]  # Compare nested address data
    
    company.refresh_from_db()
    assert company.name == "Updated Company Name"

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_delete_company(api_client, company_payload):
    company = Company.objects.create(**company_payload(as_instance=True))
    url = f"/api/construction/manager/company/{company.id}/"

    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Company.objects.filter(id=company.id).exists()
