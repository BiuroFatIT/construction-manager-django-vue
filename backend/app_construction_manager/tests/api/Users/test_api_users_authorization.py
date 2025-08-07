import pytest
from django.contrib.auth import get_user_model
from app_construction_manager.models import Company

User = get_user_model()
TEST_ORDER = 32


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_user(api_client, user_payload):
    """Test that unauthenticated requests fail"""
    # Ensure no authentication is set
    api_client.force_authenticate(user=None)
    
    payload = user_payload()
    response = api_client.post("/api/construction/manager/user/", data=payload, format='json')
    
    # Should return 401 Unauthorized
    assert response.status_code == 401
    # Check for authentication-related message in Polish or English
    detail = response.data.get("detail", "").lower()
    assert ("credentials" in detail or "authentication" in detail or 
            "uwierzytelniających" in detail or "uwierzytelnienie" in detail)


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_users(api_client):
    """Test that unauthenticated users cannot list users"""
    # Ensure no authentication is set
    api_client.force_authenticate(user=None)
    
    response = api_client.get("/api/construction/manager/user/")
    
    # Should return 401 Unauthorized
    assert response.status_code == 401


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_unauthenticated_user_cannot_get_user_detail(api_client, user_with_company):
    """Test that unauthenticated users cannot get user details"""
    # Ensure no authentication is set
    api_client.force_authenticate(user=None)
    
    response = api_client.get(f"/api/construction/manager/user/{user_with_company.id}/")
    
    # Should return 401 Unauthorized
    assert response.status_code == 401


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_from_different_company_cannot_access_users(api_client, user_payload, address, user):
    """Test company isolation - users can only see users from their company"""
    # Create two different companies
    company1 = Company.objects.create(
        name="Company 1",
        email="company1@example.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )
    
    company2 = Company.objects.create(
        name="Company 2", 
        email="company2@example.com",
        address=address,
        create_by=user,
        phone_number_1="987654321",
        timezone="UTC",
        is_active=True
    )
    
    # Create users for each company
    user1_data = user_payload(as_instance=True)
    user1_data['email'] = "user1@company1.com"
    user1_data['username'] = "User1Company1"  # Make username unique
    user1 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company1,
        **user1_data
    )
    
    user2_data = user_payload(as_instance=True)
    user2_data['email'] = "user2@company2.com"
    user2_data['username'] = "User2Company2"  # Make username unique
    user2 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company2,
        **user2_data
    )
    
    # Authenticate as user1 (company1)
    api_client.force_authenticate(user=user1)
    
    # List users - should only see users from company1
    response = api_client.get("/api/construction/manager/user/")
    assert response.status_code == 200
    
    user_emails = [u["email"] for u in response.data["results"]]
    assert user1.email in user_emails
    assert user2.email not in user_emails  # Should not see user from different company
    
    # Try to access user2 directly - should fail
    response = api_client.get(f"/api/construction/manager/user/{user2.id}/")
    assert response.status_code == 404  # User from different company should not be found


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_cannot_create_user_for_different_company(api_client, user_payload, address, user):
    """Test that user_company is enforced from authenticated user"""
    # Create two companies
    company1 = Company.objects.create(
        name="Company 1",
        email="company1@example.com", 
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )
    
    company2 = Company.objects.create(
        name="Company 2",
        email="company2@example.com",
        address=address,
        create_by=user,
        phone_number_1="987654321",
        timezone="UTC",
        is_active=True
    )
    
    # Create user in company1
    user_data = user_payload(as_instance=True)
    user1 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company1,
        **user_data
    )
    
    # Authenticate as user1
    api_client.force_authenticate(user=user1)
    
    # Try to create a user with explicit user_company set to company2
    payload = user_payload()
    payload['email'] = "newuser@company2.com"
    payload['user_company'] = company2.id  # Try to set different company
    
    response = api_client.post("/api/construction/manager/user/", data=payload, format='json')
    
    # Should succeed, but user_company should be overridden to company1
    assert response.status_code == 201
    assert response.data["user_company"] == company1.id  # Should be company1, not company2
    
    # Verify in database
    created_user = User.objects.get(email="newuser@company2.com")
    assert created_user.user_company == company1  # Should be assigned to authenticating user's company


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_cannot_update_users_from_different_company(api_client, user_payload, address, user):
    """Test that users cannot update users from different companies"""
    # Create two companies
    company1 = Company.objects.create(
        name="Company 1",
        email="company1@example.com",
        address=address,
        create_by=user,
        phone_number_1="123456789", 
        timezone="UTC",
        is_active=True
    )
    
    company2 = Company.objects.create(
        name="Company 2",
        email="company2@example.com",
        address=address,
        create_by=user,
        phone_number_1="987654321",
        timezone="UTC", 
        is_active=True
    )
    
    # Create users for each company
    user1_data = user_payload(as_instance=True)
    user1_data['email'] = "user1@company1.com"
    user1_data['username'] = "User1Update"  # Make username unique
    user1 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company1,
        **user1_data
    )
    
    user2_data = user_payload(as_instance=True) 
    user2_data['email'] = "user2@company2.com"
    user2_data['username'] = "User2Update"  # Make username unique
    user2 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company2,
        **user2_data
    )
    
    # Authenticate as user1 (company1)
    api_client.force_authenticate(user=user1)
    
    # Try to update user2 (from company2)
    update_data = {
        "first_name": "Hacked",
        "last_name": user2.last_name,
        "email": user2.email,
        "username": user2.username,
    }
    
    response = api_client.put(f"/api/construction/manager/user/{user2.id}/", data=update_data, format='json')
    
    # Should return 404 (user not found in their company scope)
    assert response.status_code == 404
    
    # Verify user2 was not modified
    user2.refresh_from_db()
    assert user2.first_name != "Hacked"


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_cannot_delete_users_from_different_company(api_client, user_payload, address, user):
    """Test that users cannot delete users from different companies"""
    # Create two companies
    company1 = Company.objects.create(
        name="Company 1",
        email="company1@example.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )
    
    company2 = Company.objects.create(
        name="Company 2", 
        email="company2@example.com",
        address=address,
        create_by=user,
        phone_number_1="987654321",
        timezone="UTC",
        is_active=True
    )
    
    # Create users for each company
    user1_data = user_payload(as_instance=True)
    user1_data['email'] = "user1@company1.com"
    user1_data['username'] = "User1Delete"  # Make username unique
    user1 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company1,
        **user1_data
    )
    
    user2_data = user_payload(as_instance=True)
    user2_data['email'] = "user2@company2.com" 
    user2_data['username'] = "User2Delete"  # Make username unique
    user2 = User.objects.create_user(
        password="TestPassword123!",
        user_company=company2,
        **user2_data
    )
    
    # Authenticate as user1 (company1)
    api_client.force_authenticate(user=user1)
    
    # Try to delete user2 (from company2)
    response = api_client.delete(f"/api/construction/manager/user/{user2.id}/")
    
    # Should return 404 (user not found in their company scope)
    assert response.status_code == 404
    
    # Verify user2 still exists
    assert User.objects.filter(id=user2.id).exists()
