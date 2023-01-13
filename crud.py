import schemas
from fastapi import HTTPException,status
from helpers import hash_password

import models
from sqlalchemy.orm import Session



class UserCrud():

    @staticmethod
    def create_user(request:schemas.User,db:Session):
        if request.password1 != request.password2:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="passwords do not match")
        if len(request.password1) < 6 :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="make password 6 characters")
        cleaned_password = hash_password(request.password1)
        new_user = models.UserModel(email=request.email,name=request.name,password=cleaned_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user