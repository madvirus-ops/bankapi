from fastapi import APIRouter,Request
import models 
from monnify.monnify import Monnify,MonnifyCredential
from dotenv import load_dotenv
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
async def monnify_webhook(request:Request):
    body = reserve.webhook(request)
    print(body)

