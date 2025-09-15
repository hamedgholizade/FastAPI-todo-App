def test_login_invalid_data_response_401(anon_client):
    payload = {
        "username":"testwronguser",
        "password":"Aa@12345"
    }
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 401
    
    payload = {
        "username":"testuser",
        "password":"Aa@AA12345516"
    }
    response = anon_client.post("/users/login", json=payload)
    assert response.status_code == 401

def test_login_response_200(anon_client):
    payload = {
        "username":"testuser",
        "password":"Aa@12345"
    }
    response = anon_client.post("/users/login",json=payload)
    assert response.status_code == 200
    assert "access" in response.json()
    assert "refresh" in response.json() 

def test_register_response_201(anon_client):
    payload = {
        "username":"hamed",
        "password":"Aa@12345",
        "password_confirm":"Aa@12345"
    }
    response = anon_client.post("/users/register",json=payload)
    assert response.status_code == 201
    