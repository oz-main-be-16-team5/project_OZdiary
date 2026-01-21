# app/db/database.py
from app.core.config import settings

# 모델 위치들을 리스트로 관리 (Aerich 인식용)
MODELS = [
    "app.models.user",
    "app.models.diary",
    "app.models.quote",
    "app.models.question",
    "app.models.bookmark",
    "app.models.user_question",
    "aerich.models",  # Aerich용 모델 추가
]

TORTOISE_CONFIG = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": MODELS,
            "default_connection": "default",
        }
    },
}
