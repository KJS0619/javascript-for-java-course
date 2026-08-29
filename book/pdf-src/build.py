#!/usr/bin/env python3
"""
자바 개발자를 위한 JavaScript 입문 - PDF 생성 스크립트

사용법:
    pip install playwright
    playwright install chromium
    python build.py

출력:
    ../javascript-book.pdf
"""

import asyncio
import os
from pathlib import Path

# Playwright 설치 확인
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwright가 설치되어 있지 않습니다.")
    print("설치: pip install playwright && playwright install chromium")
    exit(1)

# 설정
BOOK_DIR = Path(__file__).parent.parent
OUTPUT_PDF = BOOK_DIR / "javascript-book.pdf"
CHAPTERS = [
    "chapter0.html",
    "chapter1.html",
    "chapter2.html",
    "chapter3.html",
    "chapter4.html",
    "chapter5.html",
    "chapter6.html",
    "chapter7.html",
    "chapter8.html",
    "chapter9.html",
]

# 부크크 46배판 규격 (mm)
PAGE_WIDTH = 188
PAGE_HEIGHT = 263

# 합본용 CSS
COMBINED_CSS = """
<style>
@page {
    size: 188mm 263mm;
    margin: 20mm 15mm 25mm 15mm;
}

@page :first {
    margin-top: 0;
}

/* 챕터 시작은 새 페이지 */
.chapter-break {
    page-break-before: always;
}

/* 첫 챕터는 페이지 브레이크 없음 */
.chapter-break:first-child {
    page-break-before: avoid;
}

/* 헤더 숨기기 (PDF에서는 불필요) */
.masthead {
    display: none !important;
}

/* 네비게이션 숨기기 */
.chapter-nav {
    display: none !important;
}

/* 본문 폭 조정 */
.measure {
    max-width: 100% !important;
    padding: 0 !important;
}

/* 챕터 헤더 조정 */
.chapter-header {
    padding-top: 40px !important;
    border-bottom: none !important;
}

/* 코드 블록 페이지 나눔 방지 */
pre {
    page-break-inside: avoid;
}

/* 테이블 페이지 나눔 방지 */
table {
    page-break-inside: avoid;
}

/* keypoint 박스 페이지 나눔 방지 */
.keypoint, .warning {
    page-break-inside: avoid;
}

/* 인쇄용 폰트 */
body {
    font-family: "BookkMyungjo", "Apple Myungjo", Batang, serif !important;
}

h1, h2, h3, .chapter-header .num, .keypoint strong, .warning strong {
    font-family: "BookkGothic", "Apple SD Gothic Neo", sans-serif !important;
}
</style>
"""

# 폰트 face 정의
FONT_FACES = """
<style>
@font-face {
    font-family: 'BookkMyungjo';
    src: url('pdf-src/fonts/BookkMyungjo-Lt.ttf') format('truetype');
    font-weight: 300;
}
@font-face {
    font-family: 'BookkMyungjo';
    src: url('pdf-src/fonts/BookkMyungjo-Bd.ttf') format('truetype');
    font-weight: 700;
}
@font-face {
    font-family: 'BookkGothic';
    src: url('pdf-src/fonts/BookkGothic-Lt.ttf') format('truetype');
    font-weight: 300;
}
@font-face {
    font-family: 'BookkGothic';
    src: url('pdf-src/fonts/BookkGothic-Bd.ttf') format('truetype');
    font-weight: 700;
}
</style>
"""


def extract_body_content(html_path: Path) -> str:
    """HTML 파일에서 <main> 내용만 추출"""
    content = html_path.read_text(encoding="utf-8")

    # <main> 태그 내용 추출
    import re
    main_match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if main_match:
        return main_match.group(1)

    # <main>이 없으면 <body> 내용 추출
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_match:
        return body_match.group(1)

    return content


def extract_styles(html_path: Path) -> str:
    """HTML 파일에서 스타일 추출"""
    content = html_path.read_text(encoding="utf-8")

    import re
    styles = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    return "\n".join(styles)


def create_combined_html() -> str:
    """모든 챕터를 하나의 HTML로 합침"""

    # 첫 번째 챕터의 스타일 사용
    first_chapter = BOOK_DIR / CHAPTERS[0]
    base_styles = extract_styles(first_chapter)

    # 각 챕터 내용 수집
    chapters_html = []
    for i, chapter_file in enumerate(CHAPTERS):
        chapter_path = BOOK_DIR / chapter_file
        if not chapter_path.exists():
            print(f"경고: {chapter_file} 파일이 없습니다.")
            continue

        content = extract_body_content(chapter_path)

        # 첫 챕터가 아니면 페이지 브레이크 클래스 추가
        if i > 0:
            chapters_html.append(f'<div class="chapter-break">{content}</div>')
        else:
            chapters_html.append(f'<div class="chapter-break">{content}</div>')

    # 합본 HTML 생성
    combined = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>자바 개발자를 위한 JavaScript 입문</title>
    {FONT_FACES}
    <style>{base_styles}</style>
    {COMBINED_CSS}
</head>
<body>
    {"".join(chapters_html)}
</body>
</html>
"""

    return combined


async def generate_pdf():
    """PDF 생성"""
    print("PDF 생성 시작...")

    # 합본 HTML 생성
    print("1. 챕터 합치는 중...")
    combined_html = create_combined_html()

    # 임시 HTML 파일 저장
    tmp_html = BOOK_DIR / "pdf-src" / "tmp" / "combined.html"
    tmp_html.parent.mkdir(parents=True, exist_ok=True)
    tmp_html.write_text(combined_html, encoding="utf-8")
    print(f"   임시 파일: {tmp_html}")

    # Playwright로 PDF 생성
    print("2. PDF 렌더링 중...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 로컬 파일 로드
        await page.goto(f"file:///{tmp_html.resolve()}")

        # PDF 생성 (46배판: 188mm x 263mm)
        await page.pdf(
            path=str(OUTPUT_PDF),
            width=f"{PAGE_WIDTH}mm",
            height=f"{PAGE_HEIGHT}mm",
            margin={
                "top": "20mm",
                "right": "15mm",
                "bottom": "25mm",
                "left": "15mm"
            },
            print_background=True,
            display_header_footer=False,
            prefer_css_page_size=True
        )

        await browser.close()

    print(f"3. PDF 생성 완료: {OUTPUT_PDF}")
    print(f"   파일 크기: {OUTPUT_PDF.stat().st_size / 1024 / 1024:.2f} MB")


async def generate_individual_pdfs():
    """각 챕터별 개별 PDF 생성"""
    print("개별 챕터 PDF 생성...")

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for chapter_file in CHAPTERS:
            chapter_path = BOOK_DIR / chapter_file
            if not chapter_path.exists():
                continue

            page = await browser.new_page()
            await page.goto(f"file:///{chapter_path.resolve()}")

            output_path = BOOK_DIR / "pdf-src" / "tmp" / chapter_file.replace(".html", ".pdf")
            await page.pdf(
                path=str(output_path),
                width=f"{PAGE_WIDTH}mm",
                height=f"{PAGE_HEIGHT}mm",
                margin={
                    "top": "20mm",
                    "right": "15mm",
                    "bottom": "25mm",
                    "left": "15mm"
                },
                print_background=True
            )
            print(f"   {chapter_file} → {output_path.name}")

            await page.close()

        await browser.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--individual":
        asyncio.run(generate_individual_pdfs())
    else:
        asyncio.run(generate_pdf())
