from app_construction_manager.models import Company  # adjust import path
import pytest

# def test_get_company_by_id(api_client):
#     # Create a Company instance in the test database (id auto-generated)
#     company = Company.objects.create(
#         name="Test Company",
#         address="123TestSt",
#         email="test@example.com",
#         phone_number_1="1234567890"
#     )

#     # Use the generated company.id in the URL
#     response = api_client.get(f'/api/construction/manager/company/{company.id}/')

#     assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.content}"
#     assert response.data['id'] == company.id