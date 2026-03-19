from fastapi import FastAPI
from app import routers as posts_routers


app = FastAPI(title="System with cache for blog")

app.include_router(posts_routers.router)


@app.get("/")
async def root():
    return {"message": "ok"}
