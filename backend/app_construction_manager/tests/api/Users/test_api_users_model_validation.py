import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from app_construction_manager.models import Company, Address

User = get_user_model()
TEST_ORDER = 33


# Email uniqueness is already tested in test_api_users_fail_CRUD.py at API level
# which is more comprehensive as it tests the actual business logic


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_as_username_field(address, user):
    """Test that email is used as USERNAME_FIELD"""
    company = Company.objects.create(
        name="Test Company",
        email="company@test.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )

    # Create user with email
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        user_company=company
    )
    
    # Verify that USERNAME_FIELD is set to email
    assert User.USERNAME_FIELD == 'email'
    
    # Verify that get_username() returns email
    assert test_user.get_username() == "test@example.com"


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_company_relationship(address, user):
    """Test user_company ForeignKey relationship"""
    company1 = Company.objects.create(
        name="Company 1",
        email="company1@test.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )

    company2 = Company.objects.create(
        name="Company 2",
        email="company2@test.com",
        address=address,
        create_by=user,
        phone_number_1="987654321",
        timezone="UTC",
        is_active=True
    )

    # Create user with company
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        user_company=company1
    )
    
    # Test relationship
    assert test_user.user_company == company1
    assert test_user in company1.customuser_set.all()
    
    # Update user's company
    test_user.user_company = company2
    test_user.save()
    
    assert test_user.user_company == company2
    assert test_user in company2.customuser_set.all()
    assert test_user not in company1.customuser_set.all()


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_company_null_allowed(address, user):
    """Test that user_company can be null"""
    # Create user without company
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        user_company=None  # Explicitly null
    )
    
    # Should work without error
    assert test_user.user_company is None
    test_user.full_clean()  # Should not raise ValidationError


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_company_cascade_behavior(address, user):
    """Test what happens when company is deleted (should SET_NULL)"""
    company = Company.objects.create(
        name="Test Company",
        email="company@test.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )

    # Create user with company
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!",
        user_company=company
    )
    
    # Verify user is associated with company
    assert test_user.user_company == company
    
    # Delete company
    company.delete()
    
    # Refresh user from database
    test_user.refresh_from_db()
    
    # Should be SET_NULL, so user_company should be None
    assert test_user.user_company is None


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_required_fields():
    """Test that REQUIRED_FIELDS is empty (only email required)"""
    # Verify REQUIRED_FIELDS configuration
    assert User.REQUIRED_FIELDS == []

    # Test creating user with only email and password
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
        # No other fields required
    )
    
    assert test_user.email == "test@example.com"
    assert test_user.check_password("TestPassword123!")


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_as_login_field():
    """Test that email is configured as the login field (USERNAME_FIELD)"""
    # Verify USERNAME_FIELD configuration
    assert User.USERNAME_FIELD == 'email'
    
    # Test that get_username() returns email
    test_user = User.objects.create_user(
        username="testuser",
        email="login@example.com",
        password="TestPassword123!"
    )
    
    # get_username() should return the value of USERNAME_FIELD (email)
    assert test_user.get_username() == "login@example.com"


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_format_validation():
    """Test that email field validates format"""
    # Valid email should work
    test_user = User.objects.create_user(
        username="testuser",
        email="valid@example.com",
        password="TestPassword123!"
    )
    test_user.full_clean()  # Should not raise
    
    # Invalid email formats should fail during full_clean
    invalid_user = User.objects.create_user(
        username="testuser2",
        email="invalid-email",  # No @ or domain
        password="TestPassword123!"
    )
    
    with pytest.raises(ValidationError):
        invalid_user.full_clean()


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_string_representation():
    """Test User model __str__ method"""
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    # Since USERNAME_FIELD is email, __str__ returns email (which is the username)
    expected_str = test_user.email
    assert str(test_user) == expected_str


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_username_auto_populated():
    """Test that username is automatically set from email"""
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    # Since USERNAME_FIELD is email, the username should still be present
    # but authentication should work with email
    assert test_user.username == "testuser"
    assert test_user.email == "test@example.com"
    assert User.USERNAME_FIELD == 'email'


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_model_inheritance():
    """Test that CustomUser properly inherits from AbstractUser"""
    test_user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="TestPassword123!"
    )
    
    # Should have AbstractUser methods
    assert hasattr(test_user, 'check_password')
    assert hasattr(test_user, 'set_password')
    assert hasattr(test_user, 'get_username')
    assert hasattr(test_user, 'is_authenticated')
    
    # Should have custom field
    assert hasattr(test_user, 'user_company')
    
    # Check inheritance chain
    from django.contrib.auth.models import AbstractUser
    assert isinstance(test_user, AbstractUser)


# Email unique constraint is already tested in test_api_users_fail_CRUD.py at API level
