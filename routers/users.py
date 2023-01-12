from fastapi import APIRouter,status,Depends,HTTPException
from database import get_db
from sqlalchemy,orm import Session 


router = APIRouter(prefix="/api/v1/user", tags=['users'])


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user():
    pass