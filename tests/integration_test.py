import requests
import uuid

ENDPOINT= "http://localhost:8000"


def test_sign_up():
    email= uuid.uuid4().hex
    payload= {
    "display_name":"test user",
	"email": f"{email}test@Daomatcher.io",
	"password": "test@Daomatcher!"
    }
    sign_up_response= requests.post(ENDPOINT + "/api/auth/register", json=payload)
    assert sign_up_response.status_code == 200
    pass

def test_login():
    payload= {
	"email": "test@Daomatcher.io",
	"password": "test@Daomatcher!"
    }
    login_response= requests.post(ENDPOINT + "/api/auth/login", json=payload)
    assert login_response.status_code == 200
    pass


def login():
    payload = {
        "email": "test@Daomatcher.io",
        "password": "test@Daomatcher!"
    }
    response = requests.post(ENDPOINT + "/api/auth/login", json=payload)
    data = response.json()
    
    token = data['data']['token']
    user_info = data['data']['user']
    user_id = user_info['id']

    return {
        "user_id": user_id,
        "token": token
    }

def test_get_user():
    auth_data=login()

    headers = {
    "Authorization": f"Bearer {auth_data['token']}"
    }
    get_user_response= requests.get(ENDPOINT + f"/api/user/{auth_data['user_id']}", headers=headers)
    assert get_user_response.status_code == 200
    pass
    


    