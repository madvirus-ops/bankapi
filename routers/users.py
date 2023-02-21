from fastapi import APIRouter,status,Depends,UploadFile,File
from database import get_db
import schemas
import models
from helpers import get_object_or_404,get_image_url
from utils import get_current_user
import os
from dotenv import load_dotenv
load_dotenv()
from crud import UserCrud
from sqlalchemy.orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])
kuda_base_url = "https://kuda-openapi-uat.kudabank.com/v​2"
kd_secret_key = os.getenv("KUDA_API_KEY")




@router.get("/profile",status_code=status.HTTP_200_OK)
async def get_user_profile(user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
    account_balance = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == user.id).first()
    reserved_account = db.query(models.UserReservedAccount).filter(models.UserReservedAccount.user_id == user.id).all()
    # if not reserved_account:
    #     response =  {
    #         "username":user.username,
    #         "email":user.email,
    #         "phoneNumber":user.phoneNumber,
    #         "profile_image":user.profile_image,
    #         "account":{
    #             "bankname":"not available",
    #             "accountname":"not created",
    #             "accountNumber":"please create an account"  
    #         },
    #         "balance": account_balance.amount if account_balance else None
    #     }
    #     return response
    # if not account_balance or not reserved_account:
    #     response =  {
    #         "username":user.username,
    #         "email":user.email,
    #         "phoneNumber":user.phoneNumber,
    #         "profile_image":user.profile_image,
    #         "account":{
    #             "bankname":"not available",
    #             "accountname":"not created",
    #             "accountNumber":"please create an account"  
    #         },
    #         "balance": "shi shi no gum you"
    #     }
    #     return response

    response =  {
        "username":user.username,
        "email":user.email,
        "phoneNumber":user.phoneNumber,
        "profile_image":user.profile_image,
        # "account":{
        #     "bankname":reserved_account.bank_name if reserved_account else "not available",
        #     "accountname":reserved_account.AccountName if reserved_account else "not available",
        #     "accountNumber":reserved_account.AccountNumber if reserved_account else "not available",
        # },
        "account":reserved_account if reserved_account else "not available",
        "balance": account_balance.amount if account_balance else "not available"
    }
    return response

@router.get("/{id}",response_model=schemas.ShowUser)
async def get_user_and_posts(id:int, db:Session = Depends(get_db)):
    user = get_object_or_404(models.UserModel,id,db)
    return user


@router.put("/{id}")
async def update_user(id:int,request:schemas.UserUpdate,db:Session = Depends(get_db)):
    return UserCrud.update(id,db,request)


@router.post("/set-pin")
async def set_current_pin(request:schemas.SetPin, db:Session = Depends(get_db),user:dict = Depends(get_current_user)):
    if request:
        if request.pin1 == request.pin2:
            set_pin = models.UserPin(user_id = user.id, pin = request.pin2)
            db.add(set_pin)
            db.commit()
            return {"pin set successfully"}
        return {"pins do not match"}
    return {"something went wrong"}





@router.post("/upload-image",description="to upload profile image",status_code=status.HTTP_201_CREATED)
async def upload_user_profile(image: UploadFile = File(...), user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    """ route to upload and resize user's profile image"""
    file = await get_image_url(file=image,user=user)
    profile = db.query(models.UserModel).filter(models.UserModel.id == user.id).first()
    profile.profile_image = file
    db.commit()
    return {"profile_image":file}























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

