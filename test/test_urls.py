import os
from dotenv import load_dotenv

load_dotenv()
from .config import *

token = os.getenv("TEST_TOKEN")


os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"




# to run test i no need import routers since i don do app.include bla bla for main
# i just need write the full route
# i go def find better way :)


# make i store urls for here
post_url = "/api/v1/post"
auth_url = "/api/v1/auth"
bank_url = "/api/v1/core-banking"
user_url = "/api/v1/user"
vtu_url = "/api/v1/vtu"


# then make i proceed


# this not needed
def test_root_failed(client):
    response = client.get("/root")
    if response.status_code != 200:
        assert response.status_code == 404


# testing posts.py


def test_to_create_posts(client):
    data = {"title": "post 1", "body": "body"}
    response = client.post(post_url, json=data)
    assert response.status_code == 201
    assert response.json()["title"] == data["title"]


def test_create_posts_failed(client):
    data = {"title": "post 1", "body": "body"}
    response = client.post(post_url, json=data)
    if response.status_code == 201:
        assert response.json()["title"] == data["title"]
    


def test_to_get_post(client):
    response = client.get(post_url)
    assert response.status_code == 200
    print(response.json())
    # assert response.json()["items"][0]["title"]


def test_get_post_by_id_not_found(client):
    """to get by ud first create, should alway be 1"""
    data = {"title": "post 1", "body": "body"}
    response = client.post(post_url, json=data)
    response = client.get(post_url + "/1")
    assert response.status_code == 302
    assert response.json()["body"]


# testing


def test_get_bank(client):
    url = bank_url + "/banks/"
    response = client.get(url)
    assert response.status_code == 200


print("if you copy this code your laptop go crash")
print("**blows powder")


def test_create_user(client):
    data = {
        "username": "testuser",
        "email": "testuser@nofoobar.com",
        "password1": "testing",
        "first_name": "john",
        "last_name": "beans",
        "password2": "testing",
        "phoneNumber": "02020102",
    }
    url = auth_url + "/signup"
    response = client.post(url, json=data)
    assert response.status_code == 201
    assert response.json()["user"]["email"] == "testuser@nofoobar.com"


def test_send_toverified_user_email(client):
    url = auth_url + "/resend-email/?email=edwinayabie1@gmail.com"
    response = client.post(url)
    print(response.json())
    assert response.status_code == 200

def test_get_bank(client):
    url = bank_url + '/banks/flutterwave'
    response = client.get(url)
    assert response.status_code == 200


def test_get_user_acct(client):
    url = bank_url + '/user/reserveAccounts'
    response = client.get(url)
    assert response.status_code == 200

def test_get_bal(client):
    url = bank_url + '/account/balance'
    response = client.get(url)
    assert response.status_code == 200



