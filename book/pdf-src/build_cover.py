#!/usr/bin/env python3
"""
표지 PDF 생성 스크립트

사용법:
    python build_cover.py

출력:
    ../cover/cover.pdf
"""

import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright가 설치되어 있지 않습니다.")
    print("설치: pip install playwright && playwright install chromium")
    exit(1)

BOOK_DIR = Path(__file__).parent.parent
COVER_HTML = BOOK_DIR / "cover" / "cover.html"
OUTPUT_PDF = BOOK_DIR / "cover" / "cover.pdf"

# 부크크 풀커버 규격
COVER_WIDTH = 393.37  # mm
COVER_HEIGHT = 269    # mm


async def generate_cover_pdf():
    """표지 PDF 생성"""
    print("표지 PDF 생성 시작...")

    if not COVER_HTML.exists():
        print(f"오류: {COVER_HTML} 파일이 없습니다.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 표지 HTML 로드
        await page.goto(f"file:///{COVER_HTML.resolve()}")

        # PDF 생성
        await page.pdf(
            path=str(OUTPUT_PDF),
            width=f"{COVER_WIDTH}mm",
            height=f"{COVER_HEIGHT}mm",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True
        )

        await browser.close()

    print(f"표지 PDF 생성 완료: {OUTPUT_PDF}")
    print(f"크기: {COVER_WIDTH}mm x {COVER_HEIGHT}mm")
    print(f"파일 크기: {OUTPUT_PDF.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    asyncio.run(generate_cover_pdf())
