import requests
from fastapi import APIRouter,status,Depends,HTTPException
import models
from database import get_db
from sqlalchemy.orm import Session
from utils import get_current_user
import schemas
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

#test keys
py_secret_key =os.getenv("PAYSTACK_SECRET_KEY")
fl_secret_key = os.getenv("FLUTTERWAVE_SECRET_KEY")
kd_secret_key = os.getenv("KUDA_API_KEY")

router = APIRouter(prefix="/api/v1/core-banking",tags=['banking'])

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



