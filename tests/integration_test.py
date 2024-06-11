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




    