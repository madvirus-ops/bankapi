from fastapi import APIRouter,status,Depends
from database import get_db
import schemas
import models
from sqlalchemy.orm import Session
from helpers import get_object_or_404
from utils import get_current_user
from crud import BlogCrud
from fastapi_paginate import paginate,add_pagination,Page

router = APIRouter(prefix='/api/v1/post',tags=['post'])




@router.get("/",status_code=status.HTTP_200_OK,response_model=Page[schemas.ShowPosts])
async def list_post(db:Session=Depends(get_db)):
    """get all posts from db"""
    post = db.query(models.BlogModel).all()
    return paginate(post)


@router.get("/{id}",status_code=status.HTTP_302_FOUND,response_model=schemas.ShowPosts)
async def get_post_by_id(id:int,db:Session=Depends(get_db)):
    """get post by specific id"""
    post = get_object_or_404(models.BlogModel,id,db)
    return post



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ShowPosts)
async def create_post(post:schemas.Posts,user:dict = Depends(get_current_user),db:Session=Depends(get_db)):
    new_post = BlogCrud.create_post(post=post,db=db,user=user)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session= Depends(get_db)):
    return BlogCrud.delete(db,id)




@router.put("/{id}",status_code=status.HTTP_202_ACCEPTED)
async def update(id:int,request:schemas.Posts,db:Session= Depends(get_db)):
    return BlogCrud.update(db,id,request)
    

add_pagination(router)