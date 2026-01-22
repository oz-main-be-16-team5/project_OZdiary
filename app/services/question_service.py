import random
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

from app.models.question import QuestionModel
from app.models.user_question import UserQuestionModel
from app.models.user import UserModel


class QuestionService:
    @staticmethod
    async def get_random_question(user: UserModel) -> QuestionModel:
        user_id = int(user.user_id)

        now = datetime.now(timezone.utc)
        start_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_tomorrow = start_today + timedelta(days=1)

        today_record = (
            await UserQuestionModel.filter(
                user_id=user_id,
                created_at__gte=start_today,
                created_at__lt=start_tomorrow,
            )
            .order_by("-created_at")
            .first()
        )

        if today_record:
            raise HTTPException(status_code=400, detail="오늘은 이미 질문을 받았어요")

        total = await QuestionModel.all().count()
        if total == 0:
            raise HTTPException(status_code=404, detail="질문이 비어있어요")

        offset = random.randint(0, total - 1)
        question = await QuestionModel.all().offset(offset).first()
        if not question:
            raise HTTPException(status_code=404, detail="질문을 가져오지 못했어요")

        await UserQuestionModel.create(
            user_id=user_id,
            questions_id=question.id,
        )

        return question
