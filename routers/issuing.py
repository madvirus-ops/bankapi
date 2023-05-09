from fastapi import api
import requests
from fastapi import APIRouter,status,Depends,HTTPException,BackgroundTasks,Request
from ..issuing.helpers import get_webhook_signature,create_mapplerad_customer
from ..models import MappleradCustomer,UserModel


router = APIRouter(prefix="/api/v1/core-banking",tags=['banking'])

@router.post("/webhook")
async def webhook_handler(request: Request):
    body = await request.body()
    svix_id = request.headers.get("svix-id")
    svix_timestamp = request.headers.get("svix-timestamp")
    svix_signature = request.headers.get("svix-signature")

    signature = get_webhook_signature(svix_id, svix_timestamp, body)

    if signature != svix_signature:
        return JSONResponse(content={"message": "Invalid signature"}, status_code=400)
    print("webhook valid")

# 
@router.post("/create-maplerad-customer")
async def create_mapplerad_customer_endpoint(user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        return "user not fount"
    created_user =  create_mapplerad_customer(user_id=user.id, db=db)
    if not created_user:
        return "error ooooo"
    new_customer = MappleradCustomer(
        user_id = user.id,
        customer_id = created_user['data']['id']
    )
    db.add(new_customer)
    db.commit()
    return "customer created and saved"