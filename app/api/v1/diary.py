from typing import List
from fastapi import APIRouter, HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.schemas.diary import (
    DiaryResponse,
    CreateDiaryRequest,
    UpdateDiaryRequest,
    DeleteDiaryResponse,
)
from app.services.diary_service import (
    service_create_diary,
    service_get_diaries,
    service_get_diary,
    service_delete_diary,
    service_update_diary_title,
    service_update_diary_content,
)

# 라우터 생성
postgres_router = APIRouter(prefix="/v1/diary", tags=["Diary"], redirect_slashes=False)


# CREATE
@postgres_router.post(
    "/", description="일기를 생성합니다.", status_code=HTTP_201_CREATED
)
async def api_create_diary(diary_data: CreateDiaryRequest) -> DiaryResponse:
    # 미구현 : 현재 사용자 정보를 얻어 user_id 채우기
    # 임시 user_id
    temp_user_id = 1

    diary = await service_create_diary(temp_user_id, diary_data)
    # diary = await service_create_diary(diary_data)
    await diary.fetch_related("user")

    return DiaryResponse(
        id=diary.id,
        user_id=diary.user.user_id,
        title=diary.title,
        content=diary.content,
        created_at=diary.created_at,
        updated_at=diary.updated_at,
    )


# READ
@postgres_router.get("/", response_model=List[DiaryResponse])
async def api_read_diaries(user_id: int):
    # 임시 user_id
    temp_user_id = 1
    return await service_get_diaries(temp_user_id)


@postgres_router.get("/{diary_id}", response_model=DiaryResponse)
async def api_read_diary(diary_id: int):
    diary = await service_get_diary(diary_id)
    if not diary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없음"
        )
    return diary


@postgres_router.put("/{diary_id}", response_model=DiaryResponse)
async def api_update_diary(diary_id: int, diary_data: UpdateDiaryRequest):
    diary = await service_get_diary(diary_id)
    if not diary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없음"
        )

    await service_update_diary_title(diary_id, diary_data.title)

    if diary_data.content:
        await service_update_diary_content(diary_id, diary_data.content)

    updated_diary = await service_get_diary(diary_id)
    await updated_diary.fetch_related("user")

    return updated_diary


@postgres_router.delete("/{diary_id}", response_model=DeleteDiaryResponse)
async def api_delete_diary(
    diary_id: int,
):
    diary = await service_get_diary(diary_id)
    if not diary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없음"
        )

    success = await service_delete_diary(diary_id) > 0
    if not success:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail="삭제 중 오류"
        )

    return DeleteDiaryResponse(id=diary_id)
