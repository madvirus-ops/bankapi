from fastapi import APIRouter,Depends,status,BackgroundTasks,HTTPException
from utils import get_current_user
import models
import schemas
from worker import env_config
from fastapi_mail import MessageSchema,FastMail
from dotenv import load_dotenv
load_dotenv()
import os


router = APIRouter(prefix="/api/v1/vtu",tags=['virtual top up'])
cyb_key = os.getenv("CYBERDATA_KEY")


    