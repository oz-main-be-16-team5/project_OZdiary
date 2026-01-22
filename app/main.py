from fastapi import FastAPI

from app.api.v1.diary import postgres_router
from app.db.base import init_db

app = FastAPI()

init_db(app)

app.include_router(postgres_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}
