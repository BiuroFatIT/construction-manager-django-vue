import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
import time

TEST_ORDER = 21

@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_token_refresh_valid(unauthenticated_client, test_user_credentials):
    """Test that valid refresh token can get new access token"""
    # First, get initial tokens
    response = unauthenticated_client.post('/api/v1/auth/token/', data=test_user_credentials)
    assert response.status_code == status.HTTP_200_OK
    
    refresh_token = response.data['refresh']
    
    # Use refresh token to get new access token
    refresh_response = unauthenticated_client.post('/api/v1/auth/token/refresh/', 
                                                  data={'refresh': refresh_token})
    assert refresh_response.status_code == status.HTTP_200_OK
    assert 'access' in refresh_response.data
    
    # Verify new access token works
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_response.data["access"]}')
    test_response = client.get('/api/construction/manager/')
    assert test_response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_token_refresh_invalid(unauthenticated_client):
    """Test that invalid refresh token returns error"""
    invalid_refresh_token = "invalid.refresh.token"
    
    response = unauthenticated_client.post('/api/v1/auth/token/refresh/', 
                                          data={'refresh': invalid_refresh_token})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_token_refresh_missing(unauthenticated_client):
    """Test that missing refresh token returns error"""
    response = unauthenticated_client.post('/api/v1/auth/token/refresh/', data={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_access_with_expired_token(unauthenticated_client):
    """Test that expired access token returns 401"""
    # Create a client with an obviously expired/invalid token
    expired_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjAwMDAwMDAwLCJpYXQiOjE2MDAwMDAwMDAsImp0aSI6ImV4cGlyZWQiLCJ1c2VyX2lkIjoxfQ.invalid"
    
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {expired_token}')
    
    response = client.get('/api/construction/manager/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_access_without_token(unauthenticated_client):
    """Test that accessing protected endpoint without token returns 401"""
    response = unauthenticated_client.get('/api/construction/manager/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_access_with_malformed_token(unauthenticated_client):
    """Test that malformed token returns 401"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer not.a.valid.jwt.token')
    
    response = client.get('/api/construction/manager/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_access_with_wrong_token_type(unauthenticated_client, test_user_credentials):
    """Test that using refresh token as access token fails"""
    # Get tokens
    response = unauthenticated_client.post('/api/v1/auth/token/', data=test_user_credentials)
    assert response.status_code == status.HTTP_200_OK
    
    refresh_token = response.data['refresh']
    
    # Try to use refresh token as access token
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh_token}')
    
    response = client.get('/api/construction/manager/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_token_contains_required_claims(unauthenticated_client, test_user_credentials):
    """Test that JWT token contains required claims"""
    response = unauthenticated_client.post('/api/v1/auth/token/', data=test_user_credentials)
    assert response.status_code == status.HTTP_200_OK
    
    # Check that both tokens are present
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    # Tokens should be non-empty strings
    assert isinstance(response.data['access'], str)
    assert len(response.data['access']) > 50  # JWT tokens are long
    assert isinstance(response.data['refresh'], str)
    assert len(response.data['refresh']) > 50


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_concurrent_token_usage(unauthenticated_client, test_user_credentials):
    """Test that same token can be used from multiple clients simultaneously"""
    # Get token
    response = unauthenticated_client.post('/api/v1/auth/token/', data=test_user_credentials)
    access_token = response.data['access']
    
    # Create multiple clients with same token
    client1 = APIClient()
    client2 = APIClient()
    
    client1.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    client2.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    
    # Both should work
    response1 = client1.get('/api/construction/manager/')
    response2 = client2.get('/api/construction/manager/')
    
    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@pytest.mark.order(TEST_ORDER)
def test_token_reuse_after_refresh(unauthenticated_client, test_user_credentials):
    """Test behavior when using old access token after refresh"""
    # Get initial tokens
    response = unauthenticated_client.post('/api/v1/auth/token/', data=test_user_credentials)
    old_access_token = response.data['access']
    refresh_token = response.data['refresh']
    
    # Get new access token using refresh
    refresh_response = unauthenticated_client.post('/api/v1/auth/token/refresh/', 
                                                  data={'refresh': refresh_token})
    new_access_token = refresh_response.data['access']
    
    # Both old and new access tokens should work (depending on JWT implementation)
    old_client = APIClient()
    new_client = APIClient()
    
    old_client.credentials(HTTP_AUTHORIZATION=f'Bearer {old_access_token}')
    new_client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
    
    old_response = old_client.get('/api/construction/manager/')
    new_response = new_client.get('/api/construction/manager/')
    
    # New token should definitely work
    assert new_response.status_code == status.HTTP_200_OK
    
    # Old token behavior depends on implementation - document the behavior
    # Most JWT implementations allow old tokens until they expire
    print(f"Old token status: {old_response.status_code}")
