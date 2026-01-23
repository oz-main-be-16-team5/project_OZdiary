from typing import List, Optional
import random
from app.models.quote import QuoteModel  # 명언 모델 임포트


async def service_create_quote(quote_data: dict) -> tuple[QuoteModel, bool]:
    """
    명언을 생성합니다.
    동일한 내용(content)이 이미 존재하면 생성하지 않고 기존 객체를 반환합니다.
    반환값: (Quote 객체, 신규 생성 여부)
    """
    content = quote_data.get("content")
    author = quote_data.get("author")

    # 1. 중복 체크 (내용 기준)
    existing_quote = await QuoteModel.filter(content=content).first()
    if existing_quote:
        return existing_quote, False

    # 2. 신규 저장
    new_quote = await QuoteModel.create(
        content=content, author=author if author else "작자 미상"
    )
    return new_quote, True


async def service_get_random_quote() -> Optional[QuoteModel]:
    """
    DB에 저장된 명언 중 하나를 무작위로 가져옵니다.
    """
    count = await QuoteModel.all().count()
    if count == 0:
        return None

    random_index = random.randint(0, count - 1)
    return await QuoteModel.all().offset(random_index).first()


async def service_save_bulk_quotes(quotes: List[dict]) -> int:
    """
    스크레이퍼 등에서 넘어온 대량의 명언 리스트를 저장합니다.
    성공적으로 저장된(신규) 개수를 반환합니다.
    """
    saved_count = 0
    for q in quotes:
        _, created = await service_create_quote(q)
        if created:
            saved_count += 1
    return saved_count
