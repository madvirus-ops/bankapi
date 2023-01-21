from database import get_db
from sqlalchemy.orm import Session
import json
from fastapi import Depends,status,HTTPException
import models
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
load_dotenv()
from jose import jwt,JWTError
from helpers import get_user_by_id
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

SECRET_KEY='secret'
ALGORITHM='HS256'


env_config = ConnectionConfig(
    MAIL_USERNAME = os.getenv("SEND_EMAIL"),
    MAIL_PASSWORD = os.getenv("SEND_EMAIL_PASSWORD"),
    MAIL_FROM = os.getenv("SEND_EMAIL"),
    MAIL_PORT = 587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME="Melidata",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER='templates'
)

def transfer_to_wallet(db:Session,toUser,User,Amount,pin):
    
    to_user = db.query(models.UserModel).filter(models.UserModel.username == toUser).first()
    to_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == to_user.id).first()

    from_user = db.query(models.UserModel).filter(models.UserModel.id == User).first()
    from_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == from_user.id).first()
    from_pinn = db.query(models.UserPin).filter(models.UserPin.user_id == from_user.id).first()
    if not to_user_wallet:
        new = models.UserAccountBalance(user_id = to_user.id, amount = 0)
        db.add(new)
        db.commit()
        # raise HTTPException(status_code=400,detail="no balance")
    if from_pinn.pin == pin:
        
        if from_user_wallet.amount >= Amount:
            to_user_wallet.amount = to_user_wallet.amount + Amount
            from_user_wallet.amount = from_user_wallet.amount - Amount 
            db.commit()
            return {
                "message":"transfer successful",

            }
        return {
            "status":"ok",
            "message":"insuffiecient funds"
        }
    return {
        "message":"incorrect pin",
        "pin":from_pinn.pin,
        "sent":pin
    }


def verification_code(user_id):
    data={'sub':user_id, 'type':'verify_email_code', 'exp':datetime.now(tz=timezone.utc)+timedelta(minutes=15)}
    encoded=jwt.encode(data,SECRET_KEY, algorithm=ALGORITHM )
    return encoded

def verify_email_code(token, db:Session):
    exception= HTTPException(status_code=400,  detail='invalid token or token has expired')
    try:
        payload=jwt.decode(token, SECRET_KEY)
        user=get_user_by_id(db=db, id=payload.get('sub'))
        if payload.get('type') != 'verify_email_code':
            raise exception
        elif not user:
            raise exception       
    except Exception as e:
        raise exception
    user.email_verified=True
    db.commit()
    db.refresh(user)
    return True