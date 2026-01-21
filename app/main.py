from fastapi import FastAPI
from app.db.base import init_db

app = FastAPI()

init_db(app)


@app.get("/")
async def health_check():
    return {"status": "ok"}
