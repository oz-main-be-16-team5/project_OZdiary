from fastapi import APIRouter, Depends
from app.api.v1.auth import get_current_user
from app.models.user import UserModel
from app.services.question_service import QuestionService

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/random")
async def get_random_question(user: UserModel = Depends(get_current_user)):
    question = await QuestionService.get_random_question(user)

    return {
        "question_id": question.id,
        "question": question.question_text,
    }
