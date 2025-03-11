from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# 크롤링할 네이버 블로그 페이지 목록
naver_blog_urls = [
    "https://www.tistory.com/?category=travel",
    "https://www.tistory.com/?category=living",
    "https://www.tistory.com/?category=family",
    "https://www.tistory.com/?category=career",
    "https://www.tistory.com/?category=news",
    "https://www.tistory.com/?category=book",
    "https://www.tistory.com/?category=entertainment",
    "https://www.tistory.com/?category=hobby"
]

def crawl_tistory():
    # 세션 시작
    session = HTMLSession()

    # 결과 저장 리스트
    all_items = []

    # 각 페이지 크롤링 실행
    for page_num, url in enumerate(naver_blog_urls, start=1):
        print(f"🔍 티스토리 블로그 (페이지 {page_num}) 크롤링 중...")

        try:
            response = session.get(url)
    
            # JavaScript 렌더링 실행 (3초 대기)
            response.html.render(sleep=5, timeout=30)
    
            # HTML 파싱
            soup = BeautifulSoup(response.html.html, "html.parser")
    
            # 블로그 글이 포함된 div 찾기
            article_list = soup.find("div", class_="list_tistory_top")
            
            if article_list:
                articles = article_list.find_all("div", class_="item_group")
                for article in articles:
                        a_tag = article.find("a", class_="link_cont zoom_cont zoom_sm")
                        if a_tag:
                            # 블로그 글 링크 찾기 (desc 내부 a 태그의 ng-href)
                            href = urljoin(url, a_tag["href"]) if a_tag and a_tag.has_attr("href") else None
                            
                            # 썸네일 이미지 찾기
                            img_tag = a_tag.find("img")  # a 태그 내부의 img 태그 찾기
                            img_src = urljoin(url, img_tag["src"]) if img_tag and img_tag.has_attr("src") else None
                            img_src = img_src.replace("C3x2", "C318x168")
                            img_src = img_src.replace("C2x1", "C160x103")
    
                        # 제목 태그 찾기 (desc 내부의 strong 태그)
                        title_tag = article.find("strong")
                        title = title_tag.text.strip() if title_tag else "제목 없음"
    
                        if href and img_src:
                            all_items.append({"title": title, "link": href, "image": img_src})
        except Exception as e:
            print(f"🚨 페이지 {page_num} 크롤링 중 오류 발생: {e}")

        time.sleep(1)
    
    print(f"✅ 총 {len(all_items)}개의 블로그 글을 크롤링 완료!")
    return all_items

# JSON 파일로 저장
#json_file = save_json(all_items, "blog_posts.json")
#print(f"📁 JSON 파일 저장 완료: {json_file}")

