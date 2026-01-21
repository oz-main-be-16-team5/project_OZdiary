from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.db.database import TORTOISE_CONFIG

app = FastAPI()

# Tortoise ORM 등록
register_tortoise(
    app,
    config=TORTOISE_CONFIG,
    add_exception_handlers=True,
)


@app.get("/")
async def health_check():
    return {"status": "ok"}
