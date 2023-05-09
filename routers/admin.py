#fastapi imports
from fastapi import APIRouter,Depends,status,HTTPException,Cookie,Header
from sqlalchemy.orm import Session

#local imports
from fastapi_jwt_auth import AuthJWT
import models
import schemas
from database import get_db
from helpers import get_user_by_email

router = APIRouter(prefix='/api/v1/admin',tags=['admin'])



#methods
def count_all_users(db = Session):
    return len(db.query(models.UserModel).all())

def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    """
        this function uses python fastapi_jwt and its login route is api/v1/login/v2
    """

    try:
        Authorize.jwt_required()
        user_email=Authorize.get_jwt_subject()
        user = get_user_by_email(email=user_email,db=db,model=models.UserModel)
        
        return user
    except:
        raise exception



@router.get("/users",status_code=status.HTTP_200_OK)
async def get_all_users(db:Session = Depends(get_db),user:dict = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="you must be an admin")
    return count_all_users(db=db)
