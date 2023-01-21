from fastapi import APIRouter,status,HTTPException,Depends,Response,Cookie,Header,BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from helpers import get_user_by_email,verify_password
import schemas
from fastapi_mail import FastMail,MessageSchema
from fastapi.security import OAuth2PasswordRequestForm
from worker import verification_code,env_config,verify_email_code

from utils import create_access_token,SECRET_KEY,access_cookies_time,ACCESS_TOKEN_LIFETIME_MINUTES,ALGORITHM,refresh_cookies_time,REFRESH_TOKEN_LIFETIME
from fastapi_jwt_auth import AuthJWT
from crud import UserCrud
from datetime import timedelta


router = APIRouter(prefix="/api/v1/auth",tags=['auth'])

authjwt_secret_key = "random"



@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,db:Session=Depends(get_db)):
    verify = get_user_by_email(request.email,db)
    if verify:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail="user with email exists")
    new_user = UserCrud.create_user(request,db)
    token = verification_code(user_id=new_user.id)
    message = MessageSchema(
        subject="Account Verification Email",
        recipients=[new_user.email], 
        template_body={'token':token, 'user':f'{new_user.username}',},
        subtype='html',
        )
    fm = FastMail(env_config)
    await fm.send_message(message, template_name="verify_email.html")
    return {"message":"email verificatin sent","user":new_user}

@router.post('/verify-email/')
def verify_email(token:schemas.VerifyEmail, db:Session=Depends(get_db)):
    verify_email_code(token.token, db)
    return {'message': 'email sucessfuly verified'}



@router.post('/resend-email/')
def resend_email_verification_code(task:BackgroundTasks,email:str, db:Session=Depends(get_db)):
    try:
        User=get_user_by_email(email=email, db=db)
        token=verification_code(User.id)
        message=MessageSchema(
            subject='Please confirm your email address',
            recipients=[User.email],
            template_body={'token':token, 'user':f'{User.username}'},
            subtype='html'
        )
        f=FastMail(env_config)
        task.add_task(f.send_message, message, template_name='verify_email.html')
        return {'message':'verification code sent'}
    except:
        raise HTTPException(detail='user with this email does not exists', status_code=400)



@router.post("/login")
async def log_user_in(response:Response,request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = get_user_by_email(request.username,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")
    if user.email_verified == False:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="email not verified, verification email sent again!!!!")
    access_token = create_access_token(data={"sub":user.email})

    

    response.set_cookie(key="access_token",
                        value=access_token,
                        max_age=timedelta(minutes=15),
                        expires=timedelta(minutes=15))
    return {"access_token":access_token,"token_type":"bearer","user":user}



    
 
@router.post("/v2/login",)
async def login_jwt(response:Response,request:schemas.Login,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    """second route to login using schemas and also sets some shits wiht refresh and access toeken"""
    user = get_user_by_email(request.username,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")

    access_token=Authorize.create_access_token(subject=user.email, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=Authorize.create_refresh_token(subject=user.email, expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}
    # access_token = create_access_token(data={"sub":user.email}))




@router.post('/refresh-token', summary='enpoint to get new access token')
def refresh_token(response:Response,Authorization:AuthJWT=Depends(), refresh_token:str=Cookie(default=None), Bearer:str=Header(default=None)):
    '''
    To get new access token the refresh token giving during signup must be passed in the header or sent with the cookie.
    its preferable to pass to make use of the cookie because it's httponly which prevents clients from accessing it.
    '''
    exception=HTTPException(status_code=401, detail='invalid refresh token or token has expired')
    try:
        Authorization.jwt_refresh_token_required()
        current_user=Authorization.get_jwt_subject()
        access_token=Authorization.create_access_token(current_user)
        response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
        return {'access_token':access_token}
    except:
        raise exception



