from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
import schemas
import models
from helpers import get_user_by_email,get_object_or_404
from crud import UserCrud
from sqlalchemy.orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])



    

@router.get("/{id}",response_model=schemas.ShowUser)
async def get_user_and_posts(id:int, db:Session = Depends(get_db)):
    user = get_object_or_404(models.UserModel,id,db)
    return user


@router.put("/{id}")
async def update_user(id:int,request:schemas.UserUpdate,db:Session = Depends(get_db)):
    return UserCrud.update(id,db,request)


