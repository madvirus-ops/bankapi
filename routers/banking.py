import requests
from fastapi import APIRouter,status,Depends,HTTPException
import models
from database import get_db
from sqlalchemy.orm import Session
import schemas

#test keys
public_key = 'FLWPUBK_TEST-b294df3153941475432a50048484f7c0-X'
secret_key = 'FLWSECK_TEST-8f12c4531edd3b947bbdbf9810097137-X'

router = APIRouter(prefix="/api/v1/core-banking",tags=['banking'])


@router.get("/banks/flutterwave")
async def get_banks(db:Session = Depends(get_db)):
    """no longer needed"""
    Headers = { "Authorization" : f"Bearer {secret_key}" }
    url = "https://api.flutterwave.com/v3/banks/NG"

    response = requests.get(url,headers=Headers)
    data = []
    data.append(response.json())
    banks = data[0]['data']
    for key in banks:
        print(key['id'],key['code'],key['name'])
        new_data = models.Banks(bank_id=key['id'],code=key['code'],name=key['name'])
        db.add(new_data)
        db.commit()

    return banks


@router.get("/banks/")
async def get_banks_list(db:Session = Depends(get_db)):
    """return the lists of banks"""
    
    banks = db.query(models.Banks).all()
    return banks