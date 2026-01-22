from app.models.diary import DiaryModel
from app.schemas.diary import CreateDiaryRequest


# CREATE
async def service_create_diary(
    user_id: int, diary_data: CreateDiaryRequest
) -> DiaryModel:
    return await DiaryModel.create_diary(
        user_id=user_id, title=diary_data.title, content=diary_data.content
    )


# READ
async def service_get_diaries(user_id: int):
    return await DiaryModel.get_all_by_user(user_id)


async def service_get_diary(diary_id: int):
    return await DiaryModel.get_by_id(diary_id)


# UPDATE
async def service_update_diary_title(diary_id: int, title: str):
    await DiaryModel.update_diary_title(diary_id=diary_id, title=title)


async def service_update_diary_content(diary_id: int, content: str):
    await DiaryModel.update_diary_content(diary_id=diary_id, content=content)


# DELETE
async def service_delete_diary(diary_id: int):
    return await DiaryModel.delete_diary(diary_id)
