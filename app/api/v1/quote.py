from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List
import random

from app.models.bookmark import BookmarkModel
from app.models.quote import QuoteModel  # <- models와의 연동
from app.schemas.quote import (
    CreateQuoteRequest,
    QuoteResponse,
)

# ✅ auth.py 안에 있는 get_current_user를 그대로 사용
from app.api.v1.auth import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/quote", tags=["quote"])


# 1) 랜덤 명언 1개
@router.get("/random", response_model=QuoteResponse)
async def get_random_quote():
    total = await QuoteModel.all().count()
    if total == 0:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    offset = random.randrange(total)
    quote = await QuoteModel.all().offset(offset).first()

    if quote is None:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    return QuoteResponse.model_validate(quote)


# 2) 명언 생성 (스크래핑 저장용)
@router.post("", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(payload: CreateQuoteRequest):
    exists = await QuoteModel.get_or_none(
        content=payload.content,
        author=payload.author,
    )

    if exists:
        return QuoteResponse.model_validate(exists)

    quote = await QuoteModel.create(
        content=payload.content,
        author=payload.author,
    )

    return QuoteResponse.model_validate(quote)


# 3) 북마크 추가 (✅ Body로 user_id 받지 않음 / ✅ 토큰에서 유저 꺼냄)
@router.post("/{quote_id}/bookmark")
async def add_bookmark(
    quote_id: int,
    user: UserModel = Depends(get_current_user),
):
    # 1) 명언 존재 확인
    quote = await QuoteModel.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # 2) 중복 방지
    exists = await BookmarkModel.get_or_none(user=user, quote=quote)
    if exists:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "이미 북마크된 명언입니다."},
        )

    # 3) 북마크 생성
    await BookmarkModel.create(user=user, quote=quote)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "북마크에 추가되었습니다."},
    )


# 4) 북마크 조회 (✅ Query user_id 제거 / ✅ 토큰에서 유저 꺼냄)
@router.get("/bookmark", response_model=List[QuoteResponse])
async def get_bookmarks(
    user: UserModel = Depends(get_current_user),
):
    bookmarks = await BookmarkModel.filter(user=user).prefetch_related("quote")
    return [QuoteResponse.model_validate(bookmark.quote) for bookmark in bookmarks]


# 5) 북마크 해제 (✅ Query user_id 제거 / ✅ 토큰에서 유저 꺼냄)
@router.delete("/{quote_id}/bookmark")
async def delete_bookmark(
    quote_id: int,
    user: UserModel = Depends(get_current_user),
):
    # 1) 명언 존재 확인
    quote = await QuoteModel.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # 2) 북마크 존재 확인
    bookmark = await BookmarkModel.get_or_none(user=user, quote=quote)
    if not bookmark:
        raise HTTPException(status_code=404, detail="북마크가 존재하지 않습니다.")

    # 3) 삭제
    await bookmark.delete()
    return {"message": "북마크가 해제되었습니다."}
