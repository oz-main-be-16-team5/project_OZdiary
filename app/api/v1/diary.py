from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.api.v1.auth import get_user_id_by_token, get_current_user
from app.models.user import UserModel

from app.schemas.diary import (
    DiaryResponse,
    CreateDiaryRequest,
    UpdateDiaryRequest,
    DeleteDiaryResponse,
)

from app.schemas.user import UserIdByTokenRequest
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
async def api_create_diary_by_token(
    diary_data: CreateDiaryRequest, user: UserModel = Depends(get_current_user)
) -> DiaryResponse:
    """
    토큰정보를 불러와 토큰으로부터 user_id를 얻습니다
    user_id에 새로운 diary를 생성합니다.
    """
    user_id = user.user_id

    diary = await service_create_diary(user_id, diary_data)
    await diary.fetch_related("user")

    return DiaryResponse(
        id=diary.id,
        user_id=diary.user.user_id,
        title=diary.title,
        content=diary.content,
        created_at=diary.created_at,
        updated_at=diary.updated_at,
    )


@postgres_router.post(
    "/str",
    description="토큰 str값으로 일기를 생성합니다.",
    status_code=HTTP_201_CREATED,
)
async def api_create_diary_by_token_str(
    diary_data: CreateDiaryRequest,
    token: str,
) -> DiaryResponse:
    """
    발급된 토큰값을 str로 입력하면 str값에서 user_id를 얻습니다
    user_id에 새로운 diary를 생성합니다.
    """
    response = await get_user_id_by_token(UserIdByTokenRequest(token=token))
    user_id = response.user_id

    diary = await service_create_diary(user_id, diary_data)
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
async def api_read_diaries_by_token(user: UserModel = Depends(get_current_user)):
    """
    토큰정보를 불러와 토큰으로부터 user_id를 얻습니다
    user_id에 속한 diary를 불러옵니다.
    """
    user_id = user.user_id

    return await service_get_diaries(user_id)


@postgres_router.get("/str", response_model=List[DiaryResponse])
async def api_read_diaries_by_token_str(token: str):
    """
    발급된 토큰값을 str로 입력하면 str값에서 user_id를 얻습니다
    user_id에 속한 diary를 불러옵니다.
    """
    response = await get_user_id_by_token(UserIdByTokenRequest(token=token))
    user_id = response.user_id

    return await service_get_diaries(user_id)


@postgres_router.get("/{diary_id}", response_model=DiaryResponse)
async def api_read_diary(diary_id: int):
    """
    diary_id를 입력하면 해당하는 diary 객체의 정보를 불러옵니다.
    """
    diary = await service_get_diary(diary_id)
    if not diary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없음"
        )
    return diary


@postgres_router.put("/{diary_id}", response_model=DiaryResponse)
async def api_update_diary(diary_id: int, diary_data: UpdateDiaryRequest):
    """
    diary_id로 조회하고 해당 객체가 존재하면 diary_data의 정보로 업데이트 합니다.
    diary_data에는 title, content가 있습니다.
    """
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
    """
    diary_id에 해당하는 객체를 삭제합니다.
    """
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
