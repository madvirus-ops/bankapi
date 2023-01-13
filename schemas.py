from pydantic import BaseModel
from typing import List
from fastapi_jwt_auth import AuthJWT

class Posts(BaseModel):
    title:str
    body:str
    

class User(BaseModel):
    name:str
    email:str
    password1:str
    password2:str


class ShowUser(BaseModel):
    name: str
    email:str
    blogs:List

    class Config():
        orm_mode = True

class UserUpdate(BaseModel):
    name:str
    email:str


class Login(BaseModel):
    username:str
    password:str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location:set ={'cookies','headers'}
    authjwt_access_cookie_key:str='access_token'
    authjwt_refresh_cookie_key:str='refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite:str ='lax'

@AuthJWT.load_config
def get_config():
    return Settings()