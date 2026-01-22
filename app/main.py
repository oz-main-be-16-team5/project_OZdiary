from fastapi import FastAPI
from app.db.base import init_db
from app.api.v1.quote import router as quote_router

app = FastAPI()

# DB 초기화
init_db(app)

# quote API 등록
app.include_router(quote_router)

@app.get("/")
async def health_check():
    return {"status": "ok"}
