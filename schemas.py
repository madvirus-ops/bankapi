from pydantic import BaseModel


class Posts(BaseModel):
    title:str
    body:str
    

class User(BaseModel):
    name:str
    email:str
    password1:str
    password2:str


