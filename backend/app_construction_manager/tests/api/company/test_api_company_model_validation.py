import pytest
from rest_framework import status
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from app_construction_manager.models import Company, Address
from django.contrib.auth import get_user_model

User = get_user_model()

# Test order for model validation tests
TEST_ORDER = 21

@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_field_length_limits(api_client):
    """Test field length validation through API"""
    
    # Test name max length (255 chars) - should succeed
    long_name = "A" * 255
    payload = {
        "name": long_name,
        "email": "test@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
        # create_by should be auto-assigned by serializer
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    
    # Debug: Print response data if test fails
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == long_name
    
    # Test name exceeding max length (256 chars) - should fail
    too_long_name = "A" * 256
    payload["name"] = too_long_name
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_phone_number_length_limits(api_client):
    """Test phone number field length validation"""
    
    # Test phone number max length (20 chars) - should succeed
    valid_phone = "1" * 20
    payload = {
        "name": "Test Company",
        "email": "test@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": valid_phone,
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Test phone number exceeding max length (21 chars) - should fail
    invalid_phone = "1" * 21
    payload["phone_number_1"] = invalid_phone
    payload["name"] = "Test Company 2"  # Change name to avoid duplicates
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number_1" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_vat_id_length_limits(api_client):
    """Test VAT ID field length validation"""
    
    # Test VAT ID max length (10 chars) - should succeed
    valid_vat = "A" * 10
    payload = {
        "name": "Test Company VAT",
        "email": "testvat@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": valid_vat,
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Test VAT ID exceeding max length (11 chars) - should fail
    invalid_vat = "A" * 11
    payload["vat_id"] = invalid_vat
    payload["name"] = "Test Company VAT 2"  # Change name to avoid duplicates
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "vat_id" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_regon_id_length_limits(api_client):
    """Test REGON ID field length validation"""
    
    # Test REGON ID max length (14 chars) - should succeed
    valid_regon = "1" * 14
    payload = {
        "name": "Test Company REGON",
        "email": "testregon@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": valid_regon,
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Test REGON ID exceeding max length (15 chars) - should fail
    invalid_regon = "1" * 15
    payload["regon_id"] = invalid_regon
    payload["name"] = "Test Company REGON 2"  # Change name to avoid duplicates
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "regon_id" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_timezone_length_limits(api_client):
    """Test timezone field length validation"""
    
    # Test timezone max length (32 chars) - should succeed
    valid_timezone = "A" * 32
    payload = {
        "name": "Test Company Timezone",
        "email": "testtz@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": valid_timezone
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    
    # Test timezone exceeding max length (33 chars) - should fail
    invalid_timezone = "A" * 33
    payload["timezone"] = invalid_timezone
    payload["name"] = "Test Company Timezone 2"  # Change name to avoid duplicates
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "timezone" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_required_fields_validation(api_client):
    """Test that all required fields are validated"""
    
    # Test missing name
    payload = {
        "email": "test@example.com",
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    
    # Test missing email
    payload = {
        "name": "Test Company",
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    
    # Test missing phone_number_1
    payload = {
        "name": "Test Company",
        "email": "test@example.com",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number_1" in response.data


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_email_format_validation(api_client):
    """Test email format validation"""
    
    # Test invalid email formats
    invalid_emails = [
        "not-an-email",
        "@example.com",
        "test@",
        "test.example.com",
        "test@.com",
        "test@com",
        ""
    ]
    
    for invalid_email in invalid_emails:
        payload = {
            "name": f"Test Company {invalid_email}",
            "email": invalid_email,
            "address": {
                "street": "Test Street",
                "building_number": "123",
                "postal_code": "12345",
                "city": "Test City",
                "state": "Test State",
                "country": "Testland"
            },
            "phone_number_1": "123456789",
            "phone_number_2": "987654321",
            "phone_number_3": "456789123",
            "vat_id": "VAT123456",
            "regon_id": "REGON789456123",
            "is_active": True,
            "timezone": "UTC"
        }
        
        response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data, f"Email validation failed for: {invalid_email}"


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_boolean_field_validation(api_client):
    """Test boolean field validation"""
    
    # Test valid boolean values
    for is_active_value in [True, False, "true", "false", 1, 0]:
        payload = {
            "name": f"Test Company Boolean {is_active_value}",
            "email": f"test{is_active_value}@example.com",
            "address": {
                "street": "Test Street",
                "building_number": "123",
                "postal_code": "12345",
                "city": "Test City",
                "state": "Test State",
                "country": "Testland"
            },
            "phone_number_1": "123456789",
            "phone_number_2": "987654321",
            "phone_number_3": "456789123",
            "vat_id": "VAT123456",
            "regon_id": "REGON789456123",
            "is_active": is_active_value,
            "timezone": "UTC"
        }
        
        response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["is_active"] in [True, False]  # Should be normalized to boolean


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_special_characters_validation(api_client):
    """Test handling of special characters in text fields"""
    
    # Test with various special characters
    special_chars_tests = [
        {"name": "Test Company with émojis 🏢", "should_pass": True},
        {"name": "Test Company with ąćęłńóśźż", "should_pass": True},
        {"name": "Test Company with русский", "should_pass": True},
        {"name": "Test Company with 中文", "should_pass": True},
        {"name": "Test Company with symbols !@#$%^&*()", "should_pass": True},
    ]
    
    for i, test_case in enumerate(special_chars_tests):
        payload = {
            "name": test_case["name"],
            "email": f"specialchars{i}@example.com",
            "address": {
                "street": "Test Street",
                "building_number": "123",
                "postal_code": "12345",
                "city": "Test City",
                "state": "Test State",
                "country": "Testland"
            },
            "phone_number_1": "123456789",
            "phone_number_2": "987654321",
            "phone_number_3": "456789123",
            "vat_id": f"VAT{i}",
            "regon_id": f"REGON{i}",
            "is_active": True,
            "timezone": "UTC"
        }
        
        response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
        
        if test_case["should_pass"]:
            assert response.status_code == status.HTTP_201_CREATED
            assert response.data["name"] == test_case["name"]
        else:
            assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_null_and_blank_fields(api_client):
    """Test handling of required vs optional fields"""
    
    # Test company creation without required address field - should fail
    payload = {
        "name": "Test Company No Address",
        "email": "noaddress@example.com",
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
        # No address field provided - should fail since address is required
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    
    # Debug: Print response data if test fails
    if response.status_code != status.HTTP_400_BAD_REQUEST:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    # Address is required, so this should fail
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "address" in response.data
    
    # Test with address provided - should succeed
    payload_with_address = {
        "name": "Test Company With Address",
        "email": "withaddress@example.com",
        "address": {
            "street": "Test Street",
            "building_number": "123",
            "postal_code": "12345",
            "city": "Test City",
            "state": "Test State",
            "country": "Testland"
        },
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT789456",
        "regon_id": "REGON456789123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload_with_address, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["address"] is not None
    assert response.data["address"]["street"] == "Test Street"


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_company_edge_case_values(api_client):
    """Test edge case values for various fields"""
    
    # Test minimum valid values
    payload = {
        "name": "A",  # Minimum 1 character
        "email": "a@b.co",  # Minimum valid email (need at least 2 chars for TLD)
        "address": {
            "street": "A",
            "building_number": "1",
            "postal_code": "1",
            "city": "A",
            "state": "A",
            "country": "A"
        },
        "phone_number_1": "1",  # Minimum 1 character
        "phone_number_2": "2",
        "phone_number_3": "3",
        "vat_id": "V",  # Minimum 1 character
        "regon_id": "R",  # Minimum 1 character
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload, format='json')
    
    # Debug: Print response data if test fails
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.data}")
    
    assert response.status_code == status.HTTP_201_CREATED
    
    # Test empty strings (should be treated as validation errors for required fields)
    payload_empty = {
        "name": "",  # Empty string should fail
        "email": "empty@example.com",
        "phone_number_1": "123456789",
        "phone_number_2": "987654321",
        "phone_number_3": "456789123",
        "vat_id": "VAT123456",
        "regon_id": "REGON789456123",
        "is_active": True,
        "timezone": "UTC"
    }
    
    response = api_client.post("/api/construction/manager/company/", data=payload_empty, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data