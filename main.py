from fastapi import FastAPI
from routers import post
import models
from database import engine

app = FastAPI(title="Banke App",description="mimicking the backend of basic fintech app")


models.Base.metadata.create_all(bind=engine)

app.include_router(post.router)

@app.get("/")
async def home():
    return {"home":"homepage on"}
