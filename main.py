from fastapi import FastAPI
from routers import post,users,authentication,banking,webhook,virtual_tp,admin,admin_authentication,issuing
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



def include_router(app):
    app.include_router(authentication.router)
    app.include_router(post.router)
    app.include_router(users.router)
    app.include_router(banking.router)
    app.include_router(webhook.router)
    app.include_router(virtual_tp.router)
    app.include_router(admin_authentication.router)
    app.include_router(admin.router)
    app.include_router(issuing.router)


def start_application():
    app = FastAPI(title="Meli Api",description="mimicking the backend of basic virtual top up app")
    include_router(app)
    return app

app = start_application()


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]





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
    pass
    







