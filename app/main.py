from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.v1.diary import diary_router
from app.db.base import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.question import router as question_router
from app.api.v1.quote import router as quote_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# DB 초기화
init_db(app)

app.include_router(auth_router)
app.include_router(question_router)
app.include_router(diary_router)
app.include_router(quote_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 로컬 테스트용이므로 모두 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_path = os.path.join(BASE_DIR, "static")

# 만약 static 폴더가 없다면 자동으로 생성해줍니다.
if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")


@app.get("/")
async def index():
    index_file = os.path.join(static_path, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "static/index.html 파일이 없습니다. 파일을 생성해주세요."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
