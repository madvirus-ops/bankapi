from typing import Optional
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from helpers import get_user_by_email
from sqlalchemy.orm import Session
import schemas
from database import get_db



SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data:dict, expires_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    
    """
        this function uses python jose and its login route is api/v1/login
    """

    cred_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="invalid credential",
                    headers={"WWW-Authenticate":"Bearer"})
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        email:str = payload.get("sub")
        if email is None:
            raise cred_error
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise cred_error
    user = get_user_by_email(token_data.email,db)
    if user is None:
        raise cred_error
    return user


def create_uuid():
    return create_uuid