from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
import schemas
import models
from sqlalchemy.orm import Session
from helpers import get_object_or_404


router = APIRouter(prefix='/api/v1/post',tags=['post'])




@router.get("/",status_code=status.HTTP_200_OK)
async def list_post(limit=10,db:Session=Depends(get_db)):
    """get all posts from db"""
    post = db.query(models.BlogModel).limit(limit).all()
    return post


@router.get("/{id}",status_code=status.HTTP_302_FOUND)

async def get_post_by_id(id:int,db:Session=Depends(get_db)):
    """get post by specific id"""
    post = get_object_or_404(models.BlogModel,id,db)
    return post



@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_post(post:schemas.Posts,db:Session=Depends(get_db)):
    """create a new blogpost"""
    new_post = models.BlogModel(title=post.title,body=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db:Session= Depends(get_db)):
    post = db.query(models.BlogModel).filter(models.BlogModel.id == id)
    post.delete(synchronize_session=False)
    db.commit()
    return {"post deleted successfully"}




