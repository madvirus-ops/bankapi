import os
from database import get_db
from sqlalchemy.orm import Session
import hmac
import hashlib
import base64
from dotenv import load_dotenv
load_dotenv()
from models import UserModel,MappleradCustomer,VirtualCards
import requests
from dataclasses import dataclass

from datetime import datetime,date



web_secret = os.getenv("MAPLERAD_WEBHOOK_KEY")
secret_key = os.getenv('MAPLERAD_SECRET_KEY')
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

BASE_URL = "https://sandbox.api.maplerad.com/v1"




def get_webhook_signature(svix_id, svix_timestamp, body):
    signed_content = f"{svix_id}.{svix_timestamp}.{body}"
    secret_bytes = base64.b64decode(web_secret.split("_")[1])
    signature = hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()



def create_mapplerad_customer(user_id:str,db:Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return "user not found"

    url = f"{BASE_URL}/customers"

    payload = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": "test@gg.com",
        "country": "NG"
    }

    #attempt to create the customer 
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in (200,201):
        data = response.json()['data']
        return data['id']

    #if the cusomer exist, there isn's a way to get the customer using email s
    # so extract all customers and find the exact one
    elif response.json()['message'] == "customer is alcard enrolled" or response.status_code == 400:
        print("customer enrolled, how do i get the customer????")
        print(response.status_code)
        datas = None
        url = f"{BASE_URL}/customers?page=1&page_size=10"
        
        second_response = requests.get(url, headers=headers)
        
        if second_response.status_code == 200:
            datas = second_response.json()['data']
            for oned_data in datas:
                if oned_data["email"] == "test@gg.com":
    
                    return oned_data['id']

            print(datas)
            return None


        else:
            print(second_response.reason)
            return None

    else:
        print("-====-ddnj-===")
        return None



def get_create_mapplerad_customer(user_id,db:Session):
    customer = db.query(MappleradCustomer).filter(MappleradCustomer.user_id == user_id).first()
    if not customer:
        return "cusomer not found"
    return customer.customer_id



def create_mapplerad_card(card_brand:str,user_id,db:Session):
    customer = db.query(MappleradCustomer).filter(MappleradCustomer.user_id == user_id).first()
    if not customer:
        return "customer not found"
    url = f"{BASE_URL}/issuing"
    payload = {
                "customer_id": customer.customer_id,
                "type": "VIRTUAL",
                "auto_approve": True,
                "brand": card_brand.upper(),
                "amount": 200,
                "currency": "USD"
            }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in (200,201):
        print(response.json())
        return {"reference":response.json()['data']['reference'],"customer_id":customer.customer_id}
    else:
        print(response.reason,response.status_code)
        return None


def get_virtual_card(user_id:str,card_id:str,db:Session):
    customer = db.query(MappleradCustomer).filter(MappleradCustomer.user_id == user_id).first()
    if not customer:
        return "customer not found"
    url = f"{BASE_URL}/issuing/{card_id}"
    response = requests.get(url, headers=headers)

    if response.status_code in (200,201):
        print(response.json())
        return response.json()['data']
    else:
        print(response.reason)
        print(response.json())
        return None



def save_virtual_card(card_id:str,card:dict,db:Session):

    try:
        card = db.query(VirtualCards).filter(VirtualCards.card_id == card_id).first()
        if card is None:
            return False
        card.name = card['name']
        card.card_number = card['card_number']
        card.masked_pan = card['masked_pan']
        card.expiry = card['expiry']
        card.cvv = card['expiry']
        card.status = card['status']
        card.type = card['type']
        card.issuer = card['issuer']
        card.currency = card['currency']
        card.balance = card['balance']
        card.street = card['address']['street']
        card.city = card['address']['city']
        card.postal_code = card['address']['postal_code']
        card.country = card['address']['country']
        card.created_at = card['created_at']
        
        db.commit()
        return card
    except Exception as e:
        print(e)
        return False

# class Encryptor:
#     def __init__(self,key1,key2):
#         self.key1 = key1
#         self.key2 = key2
#         self.fernet = MultiFernet([Fernet(self.key1), Fernet(self.key2)])
        
    
#     def encrypt(self, message):
#         token = self.fernet.encrypt(message)
#         return {"key1":self.key1,"key2":self.key2,"encrpted_toke":token}
    
#     def decrypt(self, token):
#         message = self.fernet.decrypt(token)
#         return message.decode('utf-8')



def fund_virtual_card(user_id:str,card_id:str,amount:str,db:Session):
    try:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        virtual_card = db.query(VirtualCards).filter(VirtualCards.user_id == user_id,VirtualCards.card_id == card_id).first()
        url = f"{BASE_URL}/issuing/{card_id}/fund"

        converted_amount = int(amount) * 100

        if user.dollar_balance <= amount:
            return {
                "status":"False","code":400,
                "message":"Insufficient Funds in Dollar Balance"
            }


        payload = {"amount": converted_amount}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200 and response.json()['status'] == "true":
            #remove from the dollar balance, no webhook for fund_card
            virtual_card.balance += amount
            user.dollar_balance -= amount
            db.commit()
            return {
                "status":"Success","code":200,
                "message":"Card Funded successfully"
            }
        
        return response.json()

    except Exception as e:
        print(e)
        return None


def withdraw_virtual_card(user_id:str,card_id:str,amount:str,db:Session):
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    virtual_card = db.query(VirtualCards).filter(VirtualCards.user_id == user_id,VirtualCards.card_id == card_id).first()

    try:

        if virtual_card.balance <= amount:
            return {
                "status":"False","code":400,
                "message":"Insufficient Funds in Card Balance"
            }

        url = f"{BASE_URL}/issuing/{card_id}/withdraw"

        converted_amount = int(amount) * 100
        payload = {"amount": converted_amount }

        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200 and response.json()['status'] == "true":
            virtual_card.balance -= amount
            user.dollar_balance += amount
            
            db.commit()
            return {
                "status":"Success","code":200,
                "message":"Withdrawal successful"
            }
        
        else:
            return {
                "status":"Failed","code":400,
                "message":"Withdrawal Failed"
            }


    except Exception as e:
        print(e)
        return {
                "status":"Failed","code":400,
                "message":"Something Went Wrong"
            }


def get_all_card_transactions(user_id:str,card_id:str,start_date:date,end_date:date,page_size:str,page:str,db:Session):
    try:   
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        virtual_card = db.query(VirtualCards).filter(VirtualCards.user_id == user_id,VirtualCards.card_id == card_id).first()


        url = f"{BASE_URL}/issuing/{card_id}/transactions?start_date={start_date}&end_date={end_date}&page_size={page_size}&page={page}"

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        return None

        print(response.text)
    except Exception as e:
        print(e)
        return None



# {
#   "event": "issuing.transaction",
#   "type": "DEBIT",
#   "amount": 987,
#   "description": "NAME-CHEAP.COM*BJTYUN USA",
#   "card_id": "900d4b96-e569-8440-cg98-ade24598079e",
#   "currency": "USD",
#   "reference": "98222216-d2ba-23a4-8055-76e91b24477e",
#   "status": "SUCCESSFUL",
#   "merchant": {
#     "name": "NAME-CHEAP.COM",
#     "city": "Phoenix", 
#     "country": null, 
#   },
#   "created_at": "2023-03-01 13:06:53.498091884 +0000 UTC m=+4115.961033586",
#   "updated_at": "2023-03-01 13:06:53.498096236 +0000 UTC m=+4115.961037934"
# }

def handle_maplerad_webhook(body:list,db:Session):

    if body['event'] == "issuing.transaction":
        event_type = body['type']
        amount = body['amount']
        description = body['description']
        card_id = body['card_id']
        reference = body['reference']
        status = body['status']
        created_at = body['created_at']
        updated_at = body['updated_at']

        formated_created = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f %Z m=%f").strftime("%Y-%m-%d %H:%M:%S")
        formated_updated = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S.%f %Z m=%f").strftime("%Y-%m-%d %H:%M:%S")

        card = db.query(VirtualCards).filter(VirtualCards.card_id == card_id).first()
        card.balance -= amount
        db.commit()
    elif body['event'] == 


