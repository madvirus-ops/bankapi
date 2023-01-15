import requests
from fastapi import APIRouter,status,Depends,HTTPException
import models
from database import get_db
from sqlalchemy.orm import Session
from utils import get_current_user
import schemas
import os
from dotenv import load_dotenv
load_dotenv()

#test keys
py_secret_key =os.getenv("PAYSTACK_SECRET_KEY")
fl_secret_key = os.getenv("FLUTTERWAVE_SECRET_KEY")

router = APIRouter(prefix="/api/v1/core-banking",tags=['banking'])



@router.get("/banks/flutterwave")
async def get_banks(user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    """no longer needed"""
    
    Headers = { "Authorization" : f"Bearer {fl_secret_key}" }
    url = "https://api.flutterwave.com/v3/banks/NG"
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please Authenticate")
    response = requests.get(url,headers=Headers)
    data = []
    data.append(response.json())
    banks = data[0]['data']
    # for key in banks:
    #     print(key['id'],key['code'],key['name'])
    #     new_data = models.Banks(bank_id=key['id'],code=key['code'],name=key['name'])
    #     db.add(new_data)
    #     db.commit()

    return banks
    


@router.get("/banks/")
async def get_banks_list(user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    """return the lists of banks"""
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please Authenticate")
    banks = db.query(models.Banks).all()
    return banks



@router.post("/validateBankAccount",status_code=status.HTTP_200_OK)
async def Validate_Account(request:schemas.ValidateAccount,user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    Headers = { "Authorization" : f"Bearer {py_secret_key}" }
    url = f"https://api.paystack.co/bank/resolve?account_number={request.account_number}&bank_code={request.Bank_code}"
    bank = db.query(models.Banks).filter(models.Banks.code == request.Bank_code).first()
    try:
        response = requests.get(url=url,headers=Headers)
        res = []
        res.append(response.json())
        data = res[0]['data']
        cus_response = {
            "AccountNumber":data['account_number'],
            "Accountname":data['account_name'],
            "BankCode":request.Bank_code,
            "BankName":bank.name,
            "bank_id":bank.bank_id
        }
        return cus_response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"{e},  {response.reason}")