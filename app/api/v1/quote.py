from fastapi import APIRouter, HTTPException, status
import random

from app.models.bookmark import BookmarkModel
from app.models.quote import QuoteModel # <- models와의 연동
from app.models.user import UserModel
from app.schemas.quote import (
    CreateQuoteRequest,
    QuoteResponse,
)

router = APIRouter(prefix="/quote", tags=["quote"])

# 1) 랜덤 명언 1개
@router.get("/random", response_model=QuoteResponse) # <- schemas와의 연동(API 계약)
async def get_random_quote():
    total = await QuoteModel.all().count()  # <- db와의 연결(직접 연결X / models 통해 간접 연결)
    if total == 0:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    offset = random.randrange(total)
    quote = await QuoteModel.all().offset(offset).first()

    # <- None 방어(경쟁상황: count 후 삭제 등)
    if quote is None:
        raise HTTPException(status_code=404, detail="명언을 찾지 못했습니다.")

    # <- ORM 객체 -> Response 스키마 변환
    return QuoteResponse.model_validate(quote)

# 2) 명언 생성 (스크래핑 저장용)
@router.post("", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(payload: CreateQuoteRequest):

    # 중복 명언 저장 방지
    exists = await QuoteModel.get_or_none(
        content=payload.content,
        author=payload.author,
    )
    if exists:
        return QuoteResponse.model_validate(exists)

    # 실제 DB 저장
    quote = await QuoteModel.create(
        content=payload.content,
        author=payload.author,
    )
    return QuoteResponse.model_validate(quote)

# 3) 북마크 추가
@router.post("/{quote_id}/bookmark", status_code=status.HTTP_201_CREATED)
async def add_bookmark(
        quote_id: int,
        user_id: int,
):
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
        return  {"message": "이미 북마크된 명언입니다."}

    # 4) 북마크 생성
    await BookmarkModel.create(user=user, quote=quote)
    return {"message": "북마크에 추가되었습니다."}