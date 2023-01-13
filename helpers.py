from fastapi import status,HTTPException
from passlib.context import CryptContext
import models
from sqlalchemy.orm import Session



pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def get_object_or_404(model,id,db:Session):
    object = db.query(model).filter(model.id == id).first()
    if object:
        return object
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"object with id {id} is not foumd")



def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(hashed_password,password):
    return pwd_context.verify(hashed_password,password)



def get_user_by_email(email,db:Session):
    user = db.query(models.UserModel).filter(models.UserModel.email == email).first()
    return user
   