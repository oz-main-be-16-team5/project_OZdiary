import random
from fastapi import APIRouter, Depends
from app.api.v1.auth import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/question", tags=["question"])

QUESTION = [
    "오늘 가장 감사했던 일은?",
    "오늘 하루를 한 단어로 표현한다면?",
    "요즘 가장 많이 드는 생각은?",
    "최근에 나를 웃게 만들었던 일은?",
    "오늘 잘했다고 느낀 행동 한가지는?",
    "요즘 나를 힘들게 하는 것 은?",
]


@router.get("/random")
async def get_random_question(user: UserModel = Depends(get_current_user)):
    question = random.choice(QUESTION)
    return {"username": user.username, "question": question}
