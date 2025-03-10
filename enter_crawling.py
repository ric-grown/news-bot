from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 크롤링할 URL 목록 (남성, 여성, 키즈)
enter_urls = {
    "https://entertain.daum.net/ranking/popular",
}

def crawl_entertainment():
    # 세션 시작
    session = HTMLSession()

    # 결과 저장 리스트
    all_items = []

    # 각 카테고리에 대해 크롤링 실행
    for page_num, url in enumerate(enter_urls, start=1):
        print(f"🔍 연예 카테고리 크롤링 중...")
        
        response = session.get(url)

        # JavaScript 렌더링 실행 (3초 대기)
        response.html.render(sleep=3)

        # HTML 파싱
        soup = BeautifulSoup(response.html.html, "html.parser")

        
        # 남성과 여성: ul 하위의 li에서 추출
        ul_tag = soup.find("ol", class_="list_ranking")
        if ul_tag:
            li_tags = ul_tag.find_all("li")  # 모든 li 태그 찾기
            
            for li in li_tags:
                a_tag = li.find("a")
                href = urljoin(url, a_tag["href"]) if a_tag else None  # 상대 경로 -> 절대 경로 변환

                img_tag = li.find("img")
                img_src = urljoin(url, img_tag["src"]) if img_tag else None  # 상대 경로 -> 절대 경로 변환
                
                # 제목 태그 찾기 (desc 내부의 strong 태그)
                title_tag = li.find("strong")
                title = title_tag.text.strip() if title_tag else "제목 없음"

                if href and img_src:
                    all_items.append({"title": title, "link": href, "image": img_src})

    print(f"✅ 총 {len(all_items)}개 상품 크롤링 완료!")
    return all_items
