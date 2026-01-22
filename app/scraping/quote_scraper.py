import re
from typing import List, Optional, Tuple

import httpx
from bs4 import BeautifulSoup

BASE_URL = "https://saramro.com/quotes"

def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _split_content_author(text: str) -> Tuple[str, Optional[str]]:
    """
    명언 본문 / 작성자 분리 시도
    """
    for sep in [" - ", " - ", " - ", "\n-", "\n-"]:
        if sep in text:
            left, right = text.split(sep, 1)
            left, right = _clean_text(left), _clean_text(right)
            if left and right and len(right) <= 60:
                return left, right
    return text, None

