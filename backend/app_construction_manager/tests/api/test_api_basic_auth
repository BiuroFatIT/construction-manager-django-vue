
def test_authenticated_client_can_access_protected_endpoint(api_client):
    response = api_client.get('/api/construction/manager/company/')
    assert response.status_code == 200