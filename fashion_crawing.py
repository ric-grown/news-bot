from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 크롤링할 URL 목록 (남성, 여성, 키즈)
categories = {
    "여성": "https://shop.29cm.co.kr/best-items?category_large_code=268100100",
    "남성": "https://shop.29cm.co.kr/best-items?category_large_code=272100100",
    "키즈": "https://shop.29cm.co.kr/category/list?categoryLargeCode=290100100&categoryMediumCode=&sort=RECOMMEND&defaultSort=RECOMMEND&sortOrder=DESC&page=1",
}

def crawl_fashion():
    # 세션 시작
    session = HTMLSession()

    # 결과 저장 리스트
    all_items = []

    # 각 카테고리에 대해 크롤링 실행
    for category, url in categories.items():
        print(f"🔍 {category} 카테고리 크롤링 중...")
        
        response = session.get(url)

        # JavaScript 렌더링 실행 (3초 대기)
        response.html.render(sleep=3)

        # HTML 파싱
        soup = BeautifulSoup(response.html.html, "html.parser")

        if category in ["남성", "여성"]:
            # 남성과 여성: ul 하위의 li에서 추출
            ul_tag = soup.find("ul", class_="css-18wijj1 e1y73es30")
            if ul_tag:
                li_tags = ul_tag.find_all("li")  # 모든 li 태그 찾기
                
                for li in li_tags:
                    a_tag = li.find("a")
                    href = urljoin(url, a_tag["href"]) if a_tag else None  # 상대 경로 -> 절대 경로 변환

                    img_tag = li.find("img")
                    img_src = urljoin(url, img_tag["src"]) if img_tag else None  # 상대 경로 -> 절대 경로 변환

                    if href and img_src:
                        all_items.append({"title": " ", "link": href, "image": img_src})

        elif category == "키즈":
            # 키즈: ul 하위 div에서 추출
            ul_tag = soup.find("ul", class_="pb-60 pr-0 pt-24 css-1qmfc4p e1raok3e0")
            if ul_tag:
                div_tags = ul_tag.find_all("div", class_="mb-20 space-y-12")  # 실제 클래스명 확인 필요
                
                for div in div_tags:
                    a_tag = div.find("a")
                    href = urljoin(url, a_tag["href"]) if a_tag else None  # 상대 경로 변환

                    img_tag = div.find("img")
                    img_src = urljoin(url, img_tag["src"]) if img_tag else None  # 상대 경로 변환

                    if href and img_src:
                        all_items.append({"title": " ", "link": href, "image": img_src})

    # 🔥 남성은 15개, 여성과 키즈는 20개씩 랜덤 선택
    sampled_items = {
        "남성": random.sample(all_items["남성"], min(15, len(all_items["남성"]))),
        "여성": random.sample(all_items["여성"], min(20, len(all_items["여성"]))),
        "키즈": random.sample(all_items["키즈"], min(20, len(all_items["키즈"]))),
    }

    # 결과 합치기
    final_items = sampled_items["남성"] + sampled_items["여성"] + sampled_items["키즈"]

    print(f"✅ 총 {len(final_items)}개 상품 크롤링 완료!")
    return final_items
