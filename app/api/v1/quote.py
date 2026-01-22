from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import random

from app.models.bookmark import BookmarkModel
from app.models.quote import QuoteModel  # <- models와의 연동
from app.models.user import UserModel
from app.schemas.quote import (
    CreateQuoteRequest,
    QuoteResponse,
)

router = APIRouter(prefix="/quote", tags=["quote"])


#  북마크 요청 Body 스키마 (*user_id를 Query가 아니라 Body로 받기*)
class AddBookmarkRequest(BaseModel):
    user_id: int


# 1) 랜덤 명언 1개
@router.get("/random", response_model=QuoteResponse)  # <- schemas와의 연동(API 계약)
async def get_random_quote():
    total = await QuoteModel.all().count()  # <- db와의 연결(직접 연결X / models 통해 간접 연결)
    if total == 0:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    offset = random.randrange(total)
    quote = await QuoteModel.all().offset(offset).first()

    # <- None 방어
    if quote is None:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # <- ORM 객체 -> Response 스키마 변환
    return QuoteResponse.model_validate(quote)


# 2) 명언 생성 (스크래핑 저장용)
@router.post("", response_model=QuoteResponse)
async def create_quote(payload: CreateQuoteRequest):
    # 중복 명언 저장 방지
    exists = await QuoteModel.get_or_none(
        content=payload.content,
        author=payload.author,
    )
    if exists:
        # 중복이면 생성이 아님 -> 200
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=QuoteResponse.model_validate(exists).model_dump(),
        )

    # 실제 DB 저장
    quote = await QuoteModel.create(
        content=payload.content,
        author=payload.author,
    )

    # 신규 생성 -> 201
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=QuoteResponse.model_validate(quote).model_dump(),
    )


# 3) 북마크 추가
@router.post("/{quote_id}/bookmark")
async def add_bookmark(
    quote_id: int,
    payload: AddBookmarkRequest,  # user_id를 Body로 받음
):
    # Body에서 user_id 꺼내기
    user_id = payload.user_id

    # 1) 명언 존재 확인
    quote = await QuoteModel.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # 2) 유저 존재 확인
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾지 못했습니다.")

    # 3) 중복 방지
    exists = await BookmarkModel.get_or_none(user=user, quote=quote)
    if exists:
        # 중복이면 200(멱등 처리)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "이미 북마크된 명언입니다."},
        )

    # 4) 북마크 생성
    await BookmarkModel.create(user=user, quote=quote)

    # 신규 생성 -> 201
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "북마크에 추가되었습니다."},
    )

# 4) 북마크 조회 (내가 북마크한 명언 목록)
@router.get("/bookmark", response_model=List[QuoteResponse])
async def get_bookmarks(
        user_id: int = Query(..., description="사용자 ID"),
):
    # 1) 유저 존재 확인
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾지 못했습니다.")

    # 2) 북마크 조회
    bookmarks = await BookmarkModel.filter(user=user).prefetch_related("quote")

    # 3) 명언만 추출해서 반환
    return [
        QuoteResponse.model_validate(bookmark.quote)
        for bookmark in bookmarks
    ]

# 5) 북마크 해제
@router.delete("/{quote_id}/bookmark")
async def delete_bookmark(
        quote_id: int,
        user_id: int = Query(..., description="사용자 ID")
):
    # 1) 명언 존재 확인
    quote = await QuoteModel.get_or_none(id=quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # 2) 유저 존재 확인
    user = await UserModel.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾지 못했습니다.")

    # 3) 북마크 존재 확인
    bookmark = await BookmarkModel.get_or_none(user=user, quote=quote)
    if not bookmark:
        # 이미 해제된 상태도 에러로 처리
        raise HTTPException(status_code=404, detail="북마크가 존재하지 않습니다.")

    # 4) 삭제
    await bookmark.delete()
    return {"message": "북마크가 해제되었습니다."}

