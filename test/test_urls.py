from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



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
        
    







print("if you copy this code your laptop go crash")
print("**blows powder")
print("my charger don spoili am sad")
print("fuck"*100, end=" ")