from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

import os
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"



#to run test i no need import routers since i don do app.include bla bla for main
#i just need write the full route
#i go def find better way :)


#make i store urls for her
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
                    headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNjc1NzU5MjI4fQ.2u35gQqfiA-eT_ANyU5veUvOsPuoDGhy2X7HtcK9myQ'},
                    json=data)
    assert response.status_code == 201
    assert response.json()['title'] == data['title']



def test_to_get_post():
    response = client.get(post_url)
    assert response.status_code == 200
    assert response.json()[0]['body']




def test_get_post_by_id():
    response = client.get(post_url + '/1')
    assert response.status_code == 302
    assert response.json()['body'] 











print("if you copy this code your laptop go crash")
print("**blows powder")
print("my charger don spoili am sad")
print("fuck"*100, end=" ")