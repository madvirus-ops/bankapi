from pydantic import BaseModel
from typing import List

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