from fastapi import FastAPI
from app.db.base import init_db
from app.api.v1.auth import router as auth_router

app = FastAPI()

init_db(app)

app.include_router(auth_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}
