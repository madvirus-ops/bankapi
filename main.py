from fastapi import FastAPI
from routers import post,users,authentication,banking
import models
from database import engine

app = FastAPI(title="Banke App",description="mimicking the backend of basic fintech app")



models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(post.router)
app.include_router(users.router)
app.include_router(banking.router)

@app.get("/")
async def home():
    return {"home":"homepage on"}
