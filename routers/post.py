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




