from fastapi import FastAPI
from routers import post,users,authentication,banking,webhook,virtual_tp
import models
from database import engine

app = FastAPI(title="Meli Api",description="mimicking the backend of basic fintech app")



models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(banking.router)
app.include_router(webhook.router)
app.include_router(virtual_tp.router)

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


