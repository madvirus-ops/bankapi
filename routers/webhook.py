from fastapi import APIRouter,Request,Depends
import models 
from monnify.monnify import Monnify,MonnifyCredential
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import get_db
import json
import os

router = APIRouter(tags=['webhook'],prefix="/api/webhook")

load_dotenv()

reserve = Monnify()
wallet_id = os.getenv("WALLET_ID")
contract_code = os.getenv("CONTRACT_CODE")
mn_api_key = os.getenv("MONIFY_API_KEY")
mn_secret_key = os.getenv("MONIFY_SECRET_KEY")
monnify_credential = MonnifyCredential(mn_api_key,mn_secret_key,contract_code,wallet_id,is_live=False)

@router.post("/")
async def monnify_webhook(request:Request,db:Session = Depends(get_db)):
    body = await request.body()
    data = []
    data.append(body)
    new = json.loads(data[0])
    if new['eventType'] == "SUCCESSFUL_TRANSACTION":
        customer_email = new['eventData']['customer']['email']
        amaount = new['eventData']['amountPaid']
        user = db.query(models.UserModel).filter(models.UserModel.email == customer_email).first()
        old_balancee = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == user.id).first()
        if not old_balancee:
            new_balance = models.UserAccountBalance(user_id = user.id,amount = amaount)
            db.add(new_balance)
            db.commit()
        else:
            old_balancee.amount = old_balancee.amount + amaount
            db.commit()
        print("yesss")
    print("no")

