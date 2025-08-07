import pytest
from django.contrib.auth import get_user_model

User = get_user_model()
TEST_ORDER = 30

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_create_user(api_client, user_with_company, user_payload):
    payload = user_payload()
    response = api_client.post("/api/construction/manager/user/", data=payload, format='json')

    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}, response: {response.data}"
    assert response.data["email"] == payload["email"]


@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_get_user(api_client, user_payload):
    user_data = user_payload(as_instance=True)
    user = User.objects.create_user(password="TestPassword123!", **user_data)
    assert user is not None, "User creation failed"
    url = f"/api/construction/manager/user/{user.id}/"
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["email"] == user.email

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_update_user(api_client, user_payload):
    user_data = user_payload(as_instance=True)
    user = User.objects.create_user(**user_data)
    user.set_password("TestPassword123!")  # Set a valid password
    user.save()
    
    url = f"/api/construction/manager/user/{user.id}/"
    updated_data = user_payload()
    updated_data["first_name"] = "UpdatedName"
    response = api_client.put(url, data=updated_data, format='json')
    assert response.status_code == 200
    assert response.data["first_name"] == "UpdatedName"
    user.refresh_from_db()
    assert user.first_name == "UpdatedName"

@pytest.mark.order(TEST_ORDER)
@pytest.mark.django_db
def test_delete_user(api_client, user_payload):
    user = User.objects.create_user(**user_payload(as_instance=True))
    url = f"/api/construction/manager/user/{user.id}/"
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not User.objects.filter(id=user.id).exists()
