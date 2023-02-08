from fastapi.testclient import TestClient
from main import app
import os
from dotenv import load_dotenv
load_dotenv()

client = TestClient(app)
token = os.getenv("TEST_TOKEN")



os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"



#to run test i no need import routers since i don do app.include bla bla for main
#i just need write the full route
#i go def find better way :)


#make i store urls for here
post_url = '/api/v1/post'
auth_url = '/api/va/auth'
bank_url = '/api/v1/core-banking'
user_url = '/api/va/user'
vtu_url = '/api/v1/vtu'


#then make i proceed

def test_root_success():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json(), {"home":"homepage on"}


#this not needed
def test_root_failed():
    response = client.get("/root")
    if response.status_code != 200:
        assert response.status_code == 404
        
    

#testing posts.py

def test_to_create_posts():
    data = {"title":"post 1",
                "body":"body"}
    response = client.post(post_url,
                    headers={'Authorization': f'Bearer {token}'},
                    json=data)
    assert response.status_code == 201
    assert response.json()['title'] == data['title']




def test_create_posts_failed():
    data = {"title":"post 1",
                "body":"body"}
    response = client.post(post_url,
                    headers={'Authorization': f'Bearer h{token}'},
                    json=data)
    if response.status_code == 201:
        assert response.json()['title'] == data['title']
    assert response.status_code == 401

    



def test_to_get_post():
    response = client.get(post_url)
    assert response.status_code == 200
    print(response.json())
    assert response.json()['items'][0]['title']
    




def test_get_post_by_id():
    response = client.get(post_url + '/1')
    assert response.status_code == 302
    assert response.json()['body'] 



#testing 







print("if you copy this code your laptop go crash")
print("**blows powder")

