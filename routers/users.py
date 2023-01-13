from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
import schemas
import models
from helpers import hash_password
from sqlalchemy.orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    if request.password1 != request.password2:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="passwords do not match")
    if len(request.password1) < 6 :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="make password 8 characters")
    cleaned_password = hash_password(request.password1)
    new_user = models.UserModel(email=request.email,name=request.email,password=cleaned_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    

@router.get("/{id}",response_model=schemas.ShowUser)
async def get_user_and_posts(id:int, db:Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == id).first()
    return user
