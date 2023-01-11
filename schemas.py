from pydantic import BaseModel


class Posts(BaseModel):
    title:str
    body:str
    