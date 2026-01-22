import re
import asyncio
from typing import List, Optional, Tuple

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://saramro.com/quotes"
API_BASE = "http://127.0.0.1:8000"  # uvicorn 주소
API_ENDPOINT = f"{API_BASE}/quote"  # POST /quote

def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _split_content_author(text: str) -> Tuple[str, Optional[str]]:
    for sep in [" — ", " - ", " – ", "\n- ", "\n— "]:
        if sep in text:
            left, right = text.split(sep, 1)
            left, right = _clean_text(left), _clean_text(right)
            if left and right and len(right) <= 60:
                return left, right
    return text, None

async def scrape_quotes(page: int = 1) -> List[dict]:
    url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"
    headers = {"User-Agent": "Mozilla/5.0 (ozdiary-quote-scraper)"}

    async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    results: List[dict] = []
    rows = soup.select("table tbody tr.even, table tbody tr.odd")

    for row in rows:
        a = row.select_one("td.td_subject div.bo_tit > a")
        title = _clean_text(a.get_text()) if a else ""
        if not title:
            continue

        detail_row = row.find_next_sibling("tr")
        if not detail_row:
            continue

        td = detail_row.select_one("td")
        if not td:
            continue

        raw = td.get_text()
        detail_text = _clean_text(raw)
        if len(detail_text) < 10:
            continue

        content, author = _split_content_author(detail_text)

        if len(content) < 10:
            content = title

        results.append({"content": content, "author": author})

    # 중복 제거
    unique = {}
    for q in results:
        unique[(q["content"], q["author"])] = q

    return list(unique.values())

async def save_quotes_to_api(quotes: List[dict]) -> None:
    """
    quotes: [{"content": "...", "author": "..."}, ...]
    POST /quote 로 반복 호출
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        saved = 0
        for q in quotes:
            payload = {
                "content": q["content"],
                "author": q["author"],
            }
            try:
                resp = await client.post(API_ENDPOINT, json=payload)
                # create_quote에서 중복이면 200, 신규면 201
                if resp.status_code in (200, 201):
                    saved += 1
                else:
                    print("POST failed:", resp.status_code, resp.text)
            except Exception as e:
                print("POST exception:", e)

        print(f"POST done. attempted={len(quotes)}, ok={saved}")

if __name__ == "__main__":
    async def main():
        quotes = await scrape_quotes(page=1)
        print("scraped:", len(quotes))
        if not quotes:
            print("No quotes scraped. selector 확인 필요.")
            return
        await save_quotes_to_api(quotes)

    asyncio.run(main())
