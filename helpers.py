from fastapi import status,HTTPException,Cookie,Header,Depends
from passlib.context import CryptContext
import models
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
import uuid
from database import get_db



pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def get_object_or_404(model,id,db:Session):
    object = db.query(model).filter(model.id == id).first()
    if object:
        return object
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"object with id {id} is not foumd")



def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def get_user_by_email(email,db:Session):
    user = db.query(models.UserModel).filter(models.UserModel.email == email).first()
    return user


def get_user_by_id(id:str,db:Session):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()
    return user
   


def get_current_user2(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    """
        this function uses python fastapi_jwt and its login route is api/v1/login/v2
    """

    try:
        Authorize.jwt_required()
        user_email=Authorize.get_jwt_subject()
        user=get_user_by_email(user_email,db)
        return user
    except:
        raise exception


# def generate_uuid(name):
#     name = uuid.uuid4()
#     return name