from fastapi.testclient import TestClient
from routers import authentication,banking,post,users,virtual_tp
from main import app

# client = TestClient(app)
sec = TestClient(post.router)


def test_root():
    response = sec.get("/")
    assert response.status_code == 404
    







print("if you copy this code your laptop go crash")
print("**blows powder")
print("my charger don spoili am sad")
print("fuck"*100, end=" ")