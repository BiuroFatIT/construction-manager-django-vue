import pytest
import os
import environ
from pathlib import Path
import django
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Configure Django settings before importing anything else
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'global_project.settings')
    django.setup()

# Now we can safely import Django components
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

env = environ.Env(
    # Set default values for environment variables
    DEBUG=(bool, False),  # Default to False if not set
)

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

@pytest.fixture
def test_user_credentials():
    """
    Fixture to provide test user credentials.
    """
    return {
        "username": env("TEST_USER"),
        "password": env("TEST_USER_PASSWORD")
    }

@pytest.fixture
def user(db, test_user_credentials):
    """
    Fixture that creates a test user in the test database.
    """
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=test_user_credentials["username"]
    )
    if created:
        # Properly set the password with hashing
        user.set_password(test_user_credentials["password"])
        user.save()
    return user


@pytest.fixture
def api_client(test_user_credentials, db):
    """
    Fixture to provide an API client with real JWT authentication.
    """

    User = get_user_model()

    # Create the test user
    user, created = User.objects.get_or_create(username=test_user_credentials["username"])
    if created:
        user.set_password(test_user_credentials["password"])
        user.save()

    client = APIClient()

    # Perform real login to get token
    response = client.post('/api/v1/auth/token/', data=test_user_credentials)
    assert response.status_code == 200, f"Token auth failed: {response.content}"

    access_token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client