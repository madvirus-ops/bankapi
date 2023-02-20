from fastapi import FastAPI
from routers import post,users,authentication,banking,webhook,virtual_tp,admin,admin_authentication
import models
from database import engine
from fastapi.staticfiles import StaticFiles



app = FastAPI(title="Meli Api",description="mimicking the backend of basic fintech app")



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


