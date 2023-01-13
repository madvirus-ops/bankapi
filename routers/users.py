from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
import schemas
import models
from helpers import get_user_by_email,get_object_or_404
from crud import UserCrud
from sqlalchemy.orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    verify = get_user_by_email(request.email,db)
    if verify:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail="user with email exists")
    new_user = UserCrud.create_user(request,db)
    return new_user
    

@router.get("/{id}",response_model=schemas.ShowUser)
async def get_user_and_posts(id:int, db:Session = Depends(get_db)):
    user = get_object_or_404(models.UserModel,id,db)
    return user
