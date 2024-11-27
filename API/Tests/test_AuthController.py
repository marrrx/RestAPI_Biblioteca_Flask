def test_register_success(client):
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "Password123"
    }

    response = client.post('/api/auth/register', json=data)
    
    assert response.status_code == 201
    response_data = response.get_json()
    assert 'id' in response_data
    assert response_data['name'] == data['name']
    assert response_data['email'] == data['email']