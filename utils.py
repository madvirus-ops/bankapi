from typing import Optional
from datetime import datetime,timedelta
from jose import JWTError,jwt



SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24



def create_access_token(data:dict, expires_delta:Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithn=ALGORITHM)
    return encoded_jwt
