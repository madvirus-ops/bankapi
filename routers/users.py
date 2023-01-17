from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
import schemas
import models
from helpers import get_object_or_404,get_current_user2
from utils import get_current_user
import requests
import os
from dotenv import load_dotenv
load_dotenv()
from crud import UserCrud
from sqlalchemy.orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])
kuda_base_url = "https://kuda-openapi-uat.kudabank.com/v​2"
kd_secret_key = os.getenv("KUDA_API_KEY")


    

@router.get("/{id}",response_model=schemas.ShowUser)
async def get_user_and_posts(id:int, db:Session = Depends(get_db)):
    user = get_object_or_404(models.UserModel,id,db)
    return user


@router.put("/{id}")
async def update_user(id:int,request:schemas.UserUpdate,db:Session = Depends(get_db)):
    return UserCrud.update(id,db,request)


# @router.post("/kuda-token")
# async def get_user_token(request:schemas.KudaKey):
#     dataa = {}
#     url = 'http://kuda-openapi-uat.kudabank.com/v2.1/Account/GetToken'
#     dataa['email'] = request.email
#     headers = {
#         'Content-Type': 'application/json'
#     }
                
#     if request.api_key:
#         dataa["apiKey"] = request.api_key
#     else:
#         dataa['apiKey'] = kd_secret_key

#     data = {
#             "email":dataa['email'],
#             "apiKey":dataa['apiKey']
#         }

#     try:

#         response = requests.post(url,json=data,headers=headers)
#         # if response.status_code == 200:
#         #     return response.json()
#         # else:
#         return response.json()
#     except Exception as e:
#         return e
