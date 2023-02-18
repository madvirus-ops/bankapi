from database import get_db
from sqlalchemy.orm import Session
import json
from fastapi import Depends,status,HTTPException,BackgroundTasks
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

#tf
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

def transfer_to_wallet(db:Session,toUser,User,Amount,reason,pin,task:BackgroundTasks):

    if User.username == toUser:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"comrade {User.username}, what are you doing? why you wan send money to yourself?")
    
    to_user = db.query(models.UserModel).filter(models.UserModel.username == toUser).first()
    if not to_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with name: {toUser} not found")
    to_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == to_user.id).first()

    from_user = db.query(models.UserModel).filter(models.UserModel.id == User.id).first()
    from_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == from_user.id).first()
    from_pinn = db.query(models.UserPin).filter(models.UserPin.user_id == from_user.id).first()
    if not from_pinn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Set your pin to continue")
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

            sender_message = MessageSchema(
            subject='Transaction Alert',
            recipients=[from_user.email],
            template_body={'amount':Amount, 'user':f'{from_user.username}','receiver':to_user.username,'balance':from_user_wallet.amount,'reason':reason},
            subtype='html')

            receiver_message = MessageSchema(
            subject='Transaction Alert',
            recipients=[to_user.email],
            template_body={'amount':Amount, 'user':f'{to_user.username}','sender':from_user.username,'balance':to_user_wallet.amount,'reason':reason},
            subtype='html')

            f=FastMail(env_config)
            task.add_task(f.send_message, sender_message, template_name='sender.html')
            task.add_task(f.send_message, receiver_message, template_name='receiver.html')


            return {
                "message":"transfer successful",
                "status_code":"200",
                "amount":Amount,
                "receiver":toUser,
                "txn_charge":"free"

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


def verification_code(email):
    data={'sub':email, 'type':'verify_email_code', 'exp':datetime.now(tz=timezone.utc)+timedelta(minutes=15)}
    encoded=jwt.encode(data,SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verification_email(token, db:Session,model):
    exception= HTTPException(status_code=400,  detail='invalid token or token has expired')
    userexception= HTTPException(status_code=400,  detail='no user')
    try:
        payload = jwt.decode(token,'secret',algorithms='HS256')
        user = db.query(model).filter(model.email == payload.get('sub')).first()
        if payload.get('type') != 'verify_email_code':
            raise exception
        elif not user:
            raise userexception 
        user.email_verifies = True
        db.commit()
        return {"payload":payload,"user":user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=e)
    
    


def Otp_token(email):
    data = {
        "email":email,
        "type":"email_verification"
    }
    token = jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
    return token 


async def verify_token(token : str,db:Session):
    exception= HTTPException(status_code=400,  detail='invalid token or token has expired')
    userexception= HTTPException(status_code=400,  detail='no user')
    # try:    
    #     verify = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    #     return verify
    # except Exception as e:
    #     raise e
    # try:
    #     payload=jwt.decode(token, SECRET_KEY)
    #     user=db.query(models.UserModel).filter(models.UserModel.id == payload.get('sub')).first()
    #     if payload.get('type') != 'verify_email_code':
    #         raise exception
    #     elif not user:
    #         raise userexception       
    # except Exception as e:
    #     return e
    # user.email_verifies = True
    # try:
    #     db.commit()
    #     db.refresh(user)
    # except Exception as e:
    #     raise e
    # return user