import os
from database import get_db
from sqlalchemy.orm import Session
import hmac
import hashlib
import base64
from dotenv import load_dotenv
load_dotenv()
from models import UserModel,MappleradCustomer
import requests
from dataclasses import dataclass

web_secret = os.getenv("WEBHOOK_SECRET")
secret_key = os.getenv('MAPLERAD_SECRET_KEY')
headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }





def get_webhook_signature(svix_id, svix_timestamp, body):
    signed_content = f"{svix_id}.{svix_timestamp}.{body}"
    secret_bytes = base64.b64decode(web_secret.split("_")[1])
    signature = hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()



def create_mapplerad_customer(user_id:str,db:Session):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return "user not found"

    url = "https://sandbox.api.maplerad.com/v1/customers"

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
        url = "https://sandbox.api.maplerad.com/v1/customers?page=1&page_size=10"
        
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
    url = "https://sandbox.api.maplerad.com/v1/issuing"
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
    url = f"https://sandbox.api.maplerad.com/v1/issuing/{card_id}"
    response = requests.get(url, headers=headers)

    if response.status_code in (200,201):
        print(response.json())
        return response.json()['data']
    else:
        print(response.reason)
        return response.text

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

