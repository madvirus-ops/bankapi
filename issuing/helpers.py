import os
from database import get_db
from sqlalchemy.orm import Session
import hmac
import hashlib
import base64
from dotenv import load_dotenv
load_dotenv()
from models import UserModel
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
        "email": "maild@gogme.men",
        "country": "NG"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (200,201):
        print(response.text)
        data = response.json()['data']
        print("fuck",data)
        return data

    elif response.json()['message'] == "customer is already enrolled" or response.status_code == 400:
        print("customer enrolled, how do i get the customer????")
        print(response.status_code)
        datas = None
        url = "https://sandbox.api.maplerad.com/v1/customers?page=1&page_size=5"
        second_response = requests.get(url, headers=headers)
        if second_response.status_code == 200:
            datas = second_response.json()['data']
            for oned in datas:
                if oned["email"] == "maild@gogme.men":
                    print(oned)
                    return oned 

            return {"bad":"something bad","data":datas}

            # return datas
        else:
            print(second_response.reason)
            return second_response.reason
        # print(response.text)
    else:
        print("-====-ddnj-===")
        return response.json

