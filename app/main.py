from fastapi import FastAPI
from app.db.base import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.question import router as question_router

app = FastAPI()

init_db(app)

app.include_router(auth_router)
app.include_router(question_router)


@app.get("/")
async def health_check():
    return {"status": "ok"}
