from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends,status,HTTPException
import models
import schemas


async def transfer_to_wallet(request:schemas.InternalTransfer,db:Session):

    to_user = db.query(models.UserModel).filter(models.UserModel.username == toUser).first()

    to_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == to_user.id).first()

    from_user = db.query(models.UserModel).filter(models.UserModel.username == User).first()
    from_user_wallet = db.query(models.UserAccountBalance).filter(models.UserAccountBalance.user_id == from_user.id).first()
    if from_user.pin == pin:

        if from_user_wallet.amount >= Amount:
            to_user_wallet = to_user_wallet.amount + Amount
            from_user_wallet = from_user_wallet - Amount 
            db.commit()
            response = {
                "message":"transfer successful",

            }
        response = {
            "status":"ok",
            "message":"insuffiecient funds"
        }
    response = {
        "message":"incorrect pin"
    }
    return response