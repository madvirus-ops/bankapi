from fastapi import FastAPI
from routers import post,users,authentication,banking,webhook,virtual_tp,admin,admin_authentication
import models
from database import engine
import requests
import os
from fastapi.middleware.cors import CORSMiddleware
# from celery import Celery
# celery = Celery()
from fastapi.middleware import Middleware
from dotenv import load_dotenv
load_dotenv()
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Meli Api",description="mimicking the backend of basic virtual top up app")


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]


models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(banking.router)
app.include_router(webhook.router)
app.include_router(virtual_tp.router)
app.include_router(admin_authentication.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="./static"), name="static")
app.mount("/media/profile_image",StaticFiles(directory="./media/profile_image"),name="media")

@app.get("/")
async def home():
    res = {
        'msg':'you dey home, but the route you suppose dey na',
        'route':'/docs',
        # 'anoda_msg':'kukuruku cook that thing',
        'faq':"make i drop some faq:",
        'na_beans_i_write?':'YES',
        'e_dey_work?':'YES',
        'i_go_update?':'Maybe'
    }
    return res

app.on_event('startup')
def do_some_precheck():
    # cyb_key = os.getenv("CYBERDATA_KEY")
    # url = 'https://cyberdata.ng/api/user/'
    # headers = {
    #     'Authorization': f'Token {cyb_key}',
    #     'Content-Type': 'application/json'
    # }
    # response = requests.get(url,headers=headers)
    # if response.status_code == 200:
    #     # return response.json()
    #     print(response.json())
    # print(response.status_code,"===>",response.json())
    pass
    
