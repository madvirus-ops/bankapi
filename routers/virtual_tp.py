from fastapi import APIRouter,Depends,status,BackgroundTasks,HTTPException
from utils import get_current_user
import models
import schemas
from worker import env_config
from fastapi_mail import MessageSchema,FastMail
from dotenv import load_dotenv
load_dotenv()
import os
import requests


router = APIRouter(prefix="/api/v1/vtu",tags=['virtual top up'])
cyb_key = os.getenv("CYBERDATA_KEY")




@router.get("/user",status_code=status.HTTP_200_OK)
async def check_cyber_profile():
    url = 'https://cyberdata.ng/api/user/'

    headers = {
        'Authorization': f'Token {cyb_key}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    raise HTTPException(status_code=response.status_code,detail=f"{response.text} or {response.json()}")