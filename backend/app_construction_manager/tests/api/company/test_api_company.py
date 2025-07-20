from app_construction_manager.models import Company  # adjust import path
import pytest

# def test_get_company_by_id(api_client):
#     # Perform GET request to fetch company with ID 1
#     response = api_client.get('/api/construction/manager/company/1/', timeout=5)

#     # Assert that the request was successful
#     assert response.status_code == 200

#     # Print the full response data (for debug or inspection)
#     print("Company data:", response.data)

#     # Assert that response data contains expected keys (adjust fields to your model)
#     expected_fields = {'id', 'name', 'address', 'phone_number_1', 'phone_number_2', 'phone_number_3', 'vat_id', 'region_id', 'is_active', 'timezone', 'created_at', 'updated_at', 'create_by' }
#     assert expected_fields.issubset(response.data.keys())

#     # Optional: Assert that the ID in the response is 1
#     assert response.data['id'] == 1

def test_authenticated_client_can_access_protected_endpoint(api_client):
    # Create a Company instance in the test database (id auto-generated)
    company = Company.objects.create(
        name="Test Company",
        address="123TestSt",
        email="test@example.com",
        phone_number_1="1234567890"
    )

    # Use the generated company.id in the URL
    response = api_client.get(f'/api/construction/manager/company/{company.id}/')

    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.content}"
    assert response.data['id'] == company.id