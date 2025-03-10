from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import chardet
import time

# 크롤링할 URL 목록
enter_urls = [
    "https://news.naver.com/main/ranking/popularDay.naver"
]

def crawl_news():
    # 세션 시작
    session = HTMLSession()

    # 결과 저장 리스트
    all_items = []

    # 각 카테고리에 대해 크롤링 실행
    for page_num, url in enumerate(enter_urls, start=1):
        print(f"🔍 뉴스 카테고리 크롤링 중...")

        response = session.get(url)

        # 🔥 1. 인코딩 자동 감지 후 설정
        detected_encoding = chardet.detect(response.content)["encoding"]
        response.encoding = detected_encoding if detected_encoding else "utf-8"

        # 🔥 2. JavaScript 렌더링 실행 (3초 대기)
        response.html.render(sleep=3)

        # 🔥 3. `response.content`을 직접 `decode`하여 한글 깨짐 방지
        html_content = response.content.decode(detected_encoding, errors="replace")

        # 🔥 4. HTML 파싱
        soup = BeautifulSoup(html_content, "html.parser")

        # 메인 뉴스 랭킹 div 찾기
        main_div_tag = soup.find("div", class_="rankingnews_box_wrap")
        if main_div_tag:
            rankingnews_boxes = main_div_tag.find_all("div", class_="rankingnews_box")  # 여러 개의 뉴스 박스
            
            for box in rankingnews_boxes:
                ul_tags = box.find_all("ul", class_="rankingnews_list")  # 뉴스 리스트 ul 찾기
                
                for ul in ul_tags:
                    li_tags = ul.find_all("li")  # li 태그들 찾기
                    
                    for li in li_tags:
                    # 제목과 링크 찾기 (첫 번째 <a> 태그)
                        title_tag = li.find("a", class_="list_title")
                        title = title_tag.text.strip() if title_tag else "제목 없음"
                        link = title_tag["href"] if title_tag and title_tag.has_attr("href") else None

                        if link:
                            article_response = session.get(link)
                            article_response.html.render(sleep=3)  # JavaScript 렌더링
                            article_soup = BeautifulSoup(article_response.html.html, "html.parser")
                            
                            img_tag = article_soup.find("img", id="img1")  # id="img1"인 이미지 찾기
                            img_src = img_tag["src"] if img_tag and img_tag.has_attr("src") else None
                            
                            if not img_src:
                                img_tag = article_soup.find("img", class_="_LAZY_LOADING_INIT_HIDE")
                                img_src = img_tag["data-src"] if img_tag and img_tag.has_attr("data-src") else None

                            if img_src:
                                all_items.append({"title": title, "link": link, "image": img_src})

                            # 딜레이 추가 (과부하 방지)
                            time.sleep(1)

    print(f"✅ 총 {len(all_items)}개 상품 크롤링 완료!")
    return all_items
