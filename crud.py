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



class BlogCrud():


    @staticmethod
    def create_post(post:schemas.Posts,db:Session):
        """create a new blogpost"""
        new_post = models.BlogModel(title=post.title,body=post.body,user_id=1)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post


    @staticmethod
    def delete(db:Session,id:int,):
        post = db.query(models.BlogModel).filter(models.BlogModel.id == id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        post.delete(synchronize_session=False)
        db.commit()
        return {"post deleted successfully"}


    @staticmethod
    def update(db:Session,id:int,request):
        post = db.query(models.BlogModel).filter(models.BlogModel.id == id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")
        post.update(request.dict(exclude_unset=True))
        db.commit()
        return {"post updated"}