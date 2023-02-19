from fastapi import status,HTTPException,Cookie,Header,Depends,UploadFile,File
from passlib.context import CryptContext
import models
from sqlalchemy.orm import Session
from PIL import Image
import secrets
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



def get_user_by_email(email,db:Session,model):
    user = db.query(model).filter(model.email == email).first()
    return user


def get_user_by_id(id:int,db:Session):
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


def generate_uuid(name):
    name = uuid.uuid4()
    return name





async def get_image_url(file: UploadFile = File(...),user:dict = Depends()):
    FILEPATH = "./static/"
    filename = file.filename
    ext = filename.split(".")[1]
    if ext not in ['png', 'jpg','webp']:
        return {'status': "error", 'detail':"Image type not allowed"}
    token_name= user.username+"_"+"profile_image"+"_"+secrets.token_urlsafe(4)+"."+ext
    generated_name=FILEPATH + token_name
    file_content= await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    # PILLOW IMAGE RESIZE
    img = Image.open(generated_name)
    resized_image = img.resize(size=(500,500))
    resized_image.save(generated_name)
    
    file.close()
    file_url = generated_name[1:]
    return file_url
    