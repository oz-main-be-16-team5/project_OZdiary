from fastapi import FastAPI

from app.api.v1.diary import postgres_router
from app.db.base import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.question import router as question_router
from app.api.v1.quote import router as quote_router

app = FastAPI()

# DB 초기화
init_db(app)

app.include_router(auth_router)
app.include_router(question_router)

app.include_router(postgres_router)

# quote API 등록
app.include_router(quote_router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
