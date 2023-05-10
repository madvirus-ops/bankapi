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

web_secret = os.getenv("WEBHOOK_SECRET")
secret_key = os.getenv('MAPLERAD_SECRET_KEY')



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
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    #attempt to create the customer 
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code in (200,201):
        data = response.json()['data']
        return data['id']

    #if the cusomer exist, there isn's a way to get the customer using email s
    # so extract all customers and find the exact one
    elif response.json()['message'] == "customer is already enrolled" or response.status_code == 400:
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

