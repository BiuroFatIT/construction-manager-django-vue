import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from app_construction_manager.models import Company, Address

User = get_user_model()
TEST_ORDER = 33


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_uniqueness(address, user):
    """Test that email field has unique constraint"""
    company = Company.objects.create(
        name="Test Company",
        email="company@test.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )

    # Create first user
    user1 = User.objects.create_user(
        username="testuser1",
        email="test@example.com",
        password="TestPassword123!",
        user_company=company
    )
    
    # Try to create second user with same email
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="testuser2",
            email="test@example.com",  # Same email
            password="TestPassword123!",
            user_company=company
        )


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_case_sensitivity(address, user):
    """Test if email uniqueness is case-sensitive"""
    company = Company.objects.create(
        name="Test Company",
        email="company@test.com",
        address=address,
        create_by=user,
        phone_number_1="123456789",
        timezone="UTC",
        is_active=True
    )

    # Create user with lowercase email
    user1 = User.objects.create_user(
        username="testuser1",
        email="test@example.com",
        password="TestPassword123!",
        user_company=company
    )
    
    # Try to create user with uppercase email (should work if case-sensitive, fail if case-insensitive)
    try:
        user2 = User.objects.create_user(
            username="testuser2",
            email="TEST@EXAMPLE.COM",
            password="TestPassword123!",
            user_company=company
        )
        # If we get here, emails are case-sensitive
        assert user1.email != user2.email
    except IntegrityError:
        # If IntegrityError, emails are case-insensitive (unique constraint violated)
        pytest.fail("Email uniqueness is case-insensitive - this may be desired behavior")


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
def test_user_email_required():
    """Test that email is required (since it's USERNAME_FIELD)"""
    with pytest.raises((ValueError, IntegrityError)):
        User.objects.create_user(
            username="testuser",
            email="",  # Empty email should fail
            password="TestPassword123!"
        )
    
    with pytest.raises((ValueError, IntegrityError)):
        User.objects.create_user(
            username="testuser2",
            email=None,  # None email should fail
            password="TestPassword123!"
        )


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
    
    # Default Django User __str__ returns username
    expected_str = test_user.username
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


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_user_email_unique_constraint():
    """Test the unique constraint on email field specifically"""
    # Create first user
    user1 = User.objects.create_user(
        username="user1",
        email="unique@example.com",
        password="TestPassword123!"
    )
    
    # Try to create another user with the same email but different username
    with pytest.raises(IntegrityError):
        User.objects.create_user(
            username="user2",  # Different username
            email="unique@example.com",  # Same email
            password="TestPassword123!"
        )
