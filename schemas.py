from pydantic import BaseModel,EmailStr
from typing import List
from fastapi_jwt_auth import AuthJWT
from typing import Optional

class Posts(BaseModel):
    title:str
    body:str

  
class ShowPosts(BaseModel):
    id:int
    title:str
    body:str
    class Config():
        orm_mode = True


class User(BaseModel):
    username:str
    first_name:str
    last_name:str
    email:EmailStr
    phoneNumber:str
    password1:str
    password2:str


class ShowUser(BaseModel):
    username: str
    email:EmailStr
    blogs:List

    class Config():
        orm_mode = True

class UserUpdate(BaseModel):
    name:str
    email:EmailStr
    username:str


class Login(BaseModel):
    username:str
    password:str


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location:set ={'cookies','headers'}
    authjwt_access_cookie_key:str='access_token'
    authjwt_refresh_cookie_key:str='refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite:str ='lax'

@AuthJWT.load_config
def get_config():
    return Settings()


class TokenData(BaseModel):
    email: Optional[str] = None


class BankResponse(BaseModel):
    bank_id:int
    code:str
    name:str
    class Config():
        orm_mode = True

class ValidateAccount(BaseModel):
    Bank_code:str
    account_number:int


class VerifyEmail(BaseModel):
    token : str



class TransferFund(BaseModel):
    amount:float
    currencyCode :str
    narration :str
    beneficiaryAccountName:str
    beneficiaryAccountNumber:str
    beneficiaryBankCode: str


class KudaKey(BaseModel):
    email:str
    api_key: Optional[str] = None

class Bvnreq(BaseModel):
    bvn:str


class InternalTransfer(BaseModel):
    toUser:str
    Amount: int
    pin: int
    reason:str

class SetPin(BaseModel):
    pin1:int
    pin2:int


class BuyData(BaseModel):
    network_id:int
    mobile_number:str
    plan_id:int

class resetPassword(BaseModel):
    username: Optional[str] = None
    email:Optional[str] = None


class BanksResponse(BaseModel):
    id:int
    code:str
    name:str

    class Config():
        orm_mode = True

