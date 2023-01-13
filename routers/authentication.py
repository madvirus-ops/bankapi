from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session
from database import get_db
from helpers import get_user_by_email
import schemas
import models
from crud import UserCrud


router = APIRouter(prefix="/api/v1/auth",tags=['auth'])





@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    verify = get_user_by_email(request.email,db)
    if verify:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail="user with email exists")
    new_user = UserCrud.create_user(request,db)
    return new_user

@router.post("/login")
async def log_user_in(request:schemas.Login,db:Session = Depends(get_db)):
    user = get_user_by_email(request.email,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user doesnt exists")
    pass