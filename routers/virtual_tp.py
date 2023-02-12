from fastapi import APIRouter,Depends,status,BackgroundTasks,HTTPException
from utils import get_current_user
import models
from database import get_db
from sqlalchemy.orm import Session
import schemas
from worker import env_config
from fastapi_mail import MessageSchema,FastMail
from fastapi_paginate import Page,paginate,add_pagination
from dotenv import load_dotenv
load_dotenv()
import os
import requests



router = APIRouter(prefix="/api/v1/vtu",tags=['virtual top up'])
cyb_key = os.getenv("CYBERDATA_KEY")




@router.get("/user",status_code=status.HTTP_200_OK)
async def check_cyber_profile():
    #this endpoint doesn't work
    url = 'https://cyberdata.ng/api/user/'

    headers = {
        'Authorization': f'Token {cyb_key}',
        'Content-Type': 'application/json'
    }
    payload = {}
    # response = requests.get(url,headers=headers,data=payload)
    response = requests.request("GET",url,headers=headers,data=payload)
    if response.status_code == 200:
        return response.text
    raise HTTPException(status_code=response.status_code,detail=f"{response.text} or {response.reason} ")


@router.get("/user/transactions",description="admin use...")
async def get_all_cyber_txns():

    #to get all transactions related to me
    #madvirus no forget to move this guy to admin later
    url = 'https://cyberdata.ng/api/data/'
    headers = {
        'Authorization': f'Token {cyb_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code,detail=f"{response.text} or {response.reason} ")


@router.post("/buy-data",status_code=status.HTTP_202_ACCEPTED)
async def buy_vtu_data(request:schemas.BuyData,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):
    user_bal = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == user.id).first()
    plan = db.query(models.CyberDataPlans).filter(models.CyberDataPlans.plan_id == request.plan_id).first()
    if not user_bal and plan:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="not found")
    
    url = 'https://cyberdata.ng/api/data/'
    headers = {
        'Authorization': f'Token {cyb_key}',
        'Content-Type': 'application/json'
    }


    body = {
            "network": request.network_id,
            "mobile_number": request.mobile_number,
            "plan": request.plan_id,
            "Ported_number": True,
            "payment_medium": "MAIN WALLET" or  "SME DATA BALANCE" or "AIRTEL_CG DATA BALANCE"
        }


    if user_bal.amount >= plan.plan_price:
        response = requests.post(url,headers=headers,data=body)
        if response.status_code in (200,201):
            user_bal.amount = user_bal.amount - plan.plan_price
            db.commit()
            return response.json()
        raise HTTPException(status_code=response.status_code,detail=f"{response.text} or {response.reason} ")
    else:
        raise HTTPException(status_code=status.HTTP_402_PAYMENT_REQUIRED,detail=f"insufficient balance")

@router.get('/data-plans',response_model=Page[schemas.Dataplans],status_code=status.HTTP_200_OK)
async def get_data_price_list(db:Session = Depends(get_db)):
    plans = db.query(models.CyberDataPlans).all()
    if not plans:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no data plans")
    return paginate(plans)


@router.get('/networks',status_code=status.HTTP_200_OK)
async def get_data_price_list(db:Session = Depends(get_db)):
    networks = db.query(models.CyberDataPlans).all()
    if not networks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no data plans")
    return networks


# from bss import network,plans
# @router.post("/add networks")
# async def add_networks(db:Session = Depends(get_db)):
#     for key in network:
#         new = models.CyberNetwork(
#         name = key['network_name'],
#         network_id = int(key['network_id'])
#         )
#         db.add(new)
#         db.commit()
    
    
# @router.post("/add-plans")
# async def add_files(db:Session = Depends(get_db)):
#     for key in plans:
#         print(key['data_id'])
#         print("="*20)
#         try:
#             new = models.CyberDataPlans(
#             plan_id = key['data_id'],
#             plan_price = key['Amount'],
#             network = key['Network'],
#             size = key['Size'],
#             validity = key['Validity']
#             )
#             db.add(new)
#             db.commit()
#         except Exception as e:
#             return e.args

add_pagination(router)