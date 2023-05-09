import requests
from fastapi import APIRouter,status,Depends,HTTPException,BackgroundTasks
import models
from database import get_db
from sqlalchemy.orm import Session
from utils import get_current_user
from worker import transfer_to_wallet
import schemas
import uuid
from fastapi_paginate import Page,add_pagination,paginate
import os
from dotenv import load_dotenv
from monnify.monnify import MonnifyCredential, Monnify
load_dotenv()

#test keys
py_secret_key =os.getenv("PAYSTACK_SECRET_KEY")
fl_secret_key = os.getenv("FLUTTERWAVE_SECRET_KEY")
kd_secret_key = os.getenv("KUDA_API_KEY")
kd_email = os.getenv("KUDA_EMAIL")
mn_api_key = os.getenv("MONIFY_API_KEY")
mn_secret_key = os.getenv("MONIFY_SECRET_KEY")
wallet_id = os.getenv("WALLET_ID")
contract_code = os.getenv("CONTRACT_CODE")

#init monnify
reserve = Monnify()
monnify_credential = MonnifyCredential(mn_api_key,mn_secret_key,contract_code,wallet_id,is_live=False)


router = APIRouter(prefix="/api/v1/core-banking",tags=['banking'])


#base urls
kuda_base_url = "https://kuda-openapi-uat.kudabank.com/v​2"



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

    return "use the route "
    


@router.get("/banks/",response_model=Page[schemas.BankResponse])
async def get_banks_list(user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    """return the lists of banks"""
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please Authenticate")
    banks = db.query(models.Banks).all()
    return paginate(banks)



@router.post("/validateBankAccount",status_code=status.HTTP_200_OK)
async def Validate_Account(request:schemas.ValidateAccount,user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    Headers = { "Authorization" : f"Bearer {py_secret_key}" }
    url = f"https://api.paystack.co/bank/resolve?account_number={request.account_number}&bank_code={request.Bank_code}"
    bank = db.query(models.Banks).filter(models.Banks.code == request.Bank_code).first()
    try:
        response = requests.get(url=url,headers=Headers)
        res = []
        if response.status_code == 200:

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
        else:
            raise HTTPException(status_code=response.status_code,detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"{e}")



reference_codes = {}

@router.post("/bankTransfer")
async def transfer(request:schemas.TransferFund,user:dict = Depends(get_current_user)):
    rec_url = "https://api.paystack.co/transferrecipient"
    trf_url = "https://api.paystack.co/transfer"
    if request.beneficiaryAccountNumber in reference_codes:
        reference = reference_codes[request.beneficiaryAccountNumber]
    else:
        # Generate a unique reference code
        reference = str(uuid.uuid4())
        reference_codes[request.beneficiaryAccountNumber] = reference

    headers = {
        'Authorization': f'Bearer {py_secret_key}',
        'Content-Type': 'application/json'
    }

    data = {
        "type":"nuban",
        "name" : request.beneficiaryAccountName,
        "account_number": request.beneficiaryAccountNumber,
        "bank_code": request.beneficiaryBankCode,
        "currency": "NGN"
    }

    create_receiver = requests.post(url=rec_url,headers=headers,json=data)
    if create_receiver.status_code == 201:
        res = []
        res.append(create_receiver.json())
        recipient = res[0]['data']['recipient_code']
        trf_data = { 
                    "source": "balance", 
                    "amount": request.amount,
                    "reference": reference, 
                    "recipient": recipient, 
                    "reason": request.narration 
                }
        transfer = requests.post(trf_url,headers=headers,json=trf_data)
        if transfer.status_code == 200:
            return transfer.json()
        
        return transfer.json()

    # elif create_receiver.status_code == 200:
    #     res = []
    #     res.append(create_receiver.json())
    #     nam = res[0]['data']['recipient_code']
    #     # transfer = request.post
    #     resp = {
    #         "name":nam
    #     }
        
    #     return resp
    else:
        raise HTTPException(status_code=create_receiver.status_code,detail="something went wrong")


    

@router.post("/tranfer/flutterwave")
async def process_transfer_with_flutterwave(request:schemas.TransferFund,user:dict = Depends(get_current_user)):
    url = "https://api.flutterwave.com/v3/transfers"
    if request.beneficiaryAccountNumber in reference_codes:

        reference = reference_codes[request.beneficiaryAccountNumber]
    else:
        # Generate a unique reference code
        reference = str(uuid.uuid4())
        reference_codes[request.beneficiaryAccountNumber] = reference

    headers = {
        'Authorization': f'Bearer {fl_secret_key}',
        'Content-Type': 'application/json'
    }
    data = {
            "account_bank": request.beneficiaryBankCode,
            "account_number": request.beneficiaryAccountNumber,
            "amount": request.amount,
            "narration": request.narration,
            "currency": request.currencyCode,
            "reference": reference,
            "callback_url": "https://www.flutterwave.com/ng/",
            "debit_currency": request.currencyCode
            }
    transfer = requests.post(url,headers=headers,json=data)
    if transfer.status_code == 200:
        return transfer.json()
    else:
        raise HTTPException(status_code=transfer.status_code,detail=transfer.json())



@router.post("/virtual-account")
async def create_virtual_account(user:dict =Depends(get_current_user),db:Session = Depends(get_db)):
    Headers = { "Authorization" : f"Bearer {py_secret_key}" }
    url = "https://api.paystack.co/customer"
    acct_url = "https://api.paystack.co/dedicated_account"
    # data = { 
    #     "email": user.email,
    #     "first_name": user.first_name,
    #     "last_name": user.last_name,
    #     "phone": user.phoneNumber
    #     }
    data = { 
        "email": "cos@gmail.com",
        "first_name": "user.first_name",
        "last_name": "user.last_name",
        "phone": "09000000078"
        }
    customer = db.query(models.Customer).filter(models.Customer.user_id == user.id).first()
    if customer is None:
        #if the customer does not exist create a new customer
        try:
            create_customer = requests.post(url,headers=Headers,json=data)

            if create_customer.status_code == 200:
                res = []
                res.append(create_customer.json())
                # return res
                customer = models.Customer(user_id = user.id,customer_id = res[0]['data']['customer_code'])
                # return res
                db.add(customer)
                db.commit()
                db.refresh(customer)
            else:
                raise HTTPException(status_code=create_customer.status_code,detail=create_customer.json())
        except Exception as e:
            return e
    cus_data ={ "customer": customer.customer_id, "preferred_bank": "test-bank"}
    virtual_account = requests.post(acct_url,headers=Headers,json=cus_data)
    if virtual_account.status_code == 200:
        return virtual_account.json()
    else:
        raise HTTPException(status_code=virtual_account.status_code,detail=virtual_account.json())


#for Kuda and beyond
customer_codes = {}

@router.post("/kuda/virtual-account",status_code=status.HTTP_201_CREATED)
async def create_kuda_virtual_account(user:dict =Depends(get_current_user),db:Session = Depends(get_db)):
    #authentication
    auth_url = 'https://kuda-openapi-uat.kudabank.com/v2.1/Account/GetToken'
    auth_data = {
        "email": kd_email,
        "apiKey": kd_secret_key
    }
    auth_code = requests.post(auth_url,json=auth_data)
    if auth_code.status_code == 200:
        token = auth_code.text
        return token
    raise HTTPException(status_code=auth_code.status_code,detail="something went wrong")



account_refference = {}
@router.post("/monnify/virtual-account",status_code=status.HTTP_201_CREATED)
async def create_monify_account(request:schemas.Bvnreq,user:dict =Depends(get_current_user),db:Session = Depends(get_db)):
    #first authenticate
    #  bank = reserve.verify_account(
    #    monnify_credential, 
    #    accountNumber='3121248964', 
    #    bankCode='011'
    #    )
    if user.email in reference_codes:
        reference =account_refference[user.email]
    else:
            # Generate a unique reference code
            reference = str(uuid.uuid4())
            account_refference[user.email] = reference
    #  print(bank)
    data = []
    try:
        reserve_account =  reserve.reserve_account( 
        monnify_credential, 
        accountReference=reference, 
        accountName=f"{user.first_name} {user.last_name}", 
        customerEmail=user.email, 
        customerName=f"{user.first_name} {user.last_name}", 
        customerBvn= request.bvn,
        availableBank=True
        )
    except Exception as e:
        raise HTTPException(status_code=403,detail=e.args)
    data.append(reserve_account)
    # accounts = []
    accounts = data[0]["responseBody"]["accounts"]
    # accounts.append(data[0]["responseBody"]["accountReference"])
    # return accounts
    for key in accounts:
        add_account = models.UserReservedAccount(
                user_id = user.id,
                bank_code = key["bankCode"],
                bank_name= key["bankName"],
                AccountName = key["accountName"],
                AccountNumber = key["accountNumber"],

            )
        db.add(add_account)
        db.commit()
    acct_ref = models.AccountRef(user_id = user.id,accountReference= data[0]["responseBody"]["accountReference"])
    db.add(acct_ref)
    db.commit()
    db.refresh(acct_ref)

    
    return {"reference":acct_ref,"accounts":accounts}

    print(reserve_account)
 
@router.get("/user/reserveAccounts", summary="get the account associated with this user", status_code=status.HTTP_200_OK)
def acct(user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    accounts = db.query(models.UserReservedAccount).filter(models.UserReservedAccount.user_id == user.id).all()
    ref = db.query(models.AccountRef).filter(models.AccountRef.user_id == user.id).all()
    return {"reference":ref,"accounts":accounts}


@router.get("/account/balance",summary="get the user account balance", status_code=status.HTTP_200_OK)
async def check_balance(user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    balance = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == user.id).first()
    if not balance:
        balance = models.UserAccountBalance(user_id=user.id,amount=5000)
        db.add(balance)
        db.commit()
        db.refresh(balance)
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no account balance associated with user")
    return {
        "user_email":user.email,
        "balance": f"₦{balance.amount}",
        "broke?":"Not yet"
    }



@router.post("/internal/transfer",status_code=status.HTTP_202_ACCEPTED)
async def internal_wallet_transfer(request:schemas.InternalTransfer,task:BackgroundTasks,user:dict = Depends(get_current_user),db:Session = Depends(get_db)):
    if request:
        response = transfer_to_wallet(db=db,toUser=request.toUser,User=user,Amount=request.Amount,pin=request.pin,task=task,reason=request.reason)
        return response

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="something went wrong shithead...")


add_pagination(router)