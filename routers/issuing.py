
import requests
from fastapi import APIRouter,status,Depends,HTTPException,BackgroundTasks,Request
from issuing.helpers import get_webhook_signature,create_mapplerad_customer,create_mapplerad_card,get_virtual_card,save_virtual_card
from models import MappleradCustomer,UserModel,VirtualCards
from utils import get_current_user
from database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1/card",tags=['issuing'])

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
    if created_user is None:
        raise HTTPException(400,detail="customer is not")
    print(created_user)
    new_customer = MappleradCustomer(
        user_id = user.id,
        customer_id = created_user
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
    # return created_user
@router.post("/create-card")
async def create_virtual_card(user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise "user not found"
    ready = create_mapplerad_card(user_id=user.id, db=db,card_brand="mastercard")
    if ready is None:
        return "something went wrong"
    new_card = VirtualCards(
        user_id = user.id,
        card_id = ready['reference'],
        customer_id = ready['customer_id']
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
        
    return new_card

@router.get("/get-card")
async def get_virtual_card_details(card_id:str,user:dict= Depends(get_current_user),db:Session = Depends(get_db)):
    if not user:
        raise "user not found"
    ready = get_virtual_card(user_id=user.id, card_id=card_id, db=db)
    customer = db.query(MappleradCustomer).filter(MappleradCustomer.user_id == user.id).first()
    if not customer:
        return "customer not found"
    if ready is None:
        return False
    card = db.query(VirtualCards).filter(VirtualCards.card_id == card_id).first()
    if card is None:
        new_card = VirtualCards(
            user_id = user.id,
            customer_id = customer.customer_id,
               card_name = ready['name'],
                card_number = ready['card_number'],
                masked_pan = ready['masked_pan'],
                expiry = ready['expiry'],
                cvv = ready['expiry'],
                status = ready['status'],
                card_type = ready['type'],
                issuer = ready['issuer'],
                currency = ready['currency'],
                balance = ready['balance'],
                street = ready['address']['street'],
                city = ready['address']['city'],
                postal_code = ready['address']['postal_code'],
                country = ready['address']['country'],
                created_at = ready['created_at'],
        )
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        return new_card

    update = save_virtual_card(card_id=card_id, card=ready, db=db)
    if update is False:
        return "updating failed"
    return update

