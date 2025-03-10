from requests_html import HTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 크롤링할 네이버 블로그 페이지 목록
naver_blog_urls = [
    "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0",
    "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=2&groupId=0",
    "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=3&groupId=0"
]

def crawl_blog():
    # 세션 시작
    session = HTMLSession()

    # 결과 저장 리스트
    all_items = []

    # 각 페이지 크롤링 실행
    for page_num, url in enumerate(naver_blog_urls, start=1):
        print(f"🔍 네이버 블로그 (페이지 {page_num}) 크롤링 중...")
        
        response = session.get(url)

        # JavaScript 렌더링 실행 (3초 대기)
        response.html.render(sleep=3)

        # HTML 파싱
        soup = BeautifulSoup(response.html.html, "html.parser")

        # 블로그 글이 포함된 div 찾기
        article_list = soup.find("div", class_="list_post_article")
        
        if article_list:
            articles = article_list.find_all("div", class_="item multi_pic")
            for article in articles:
                desc_tag = article.find("div", class_="desc")  # 설명이 포함된 div 찾기
                thumbnail_area = article.find("div", class_="thumbnail_area")
                
                if desc_tag:
                    # 블로그 글 링크 찾기 (desc 내부 a 태그의 ng-href)
                    a_tag = desc_tag.find("a")
                    href = urljoin(url, a_tag["ng-href"]) if a_tag and a_tag.has_attr("ng-href") else None

                    # 제목 태그 찾기 (desc 내부의 strong 태그)
                    title_tag = desc_tag.find("strong")
                    title = title_tag.text.strip() if title_tag else "제목 없음"

                    # 썸네일 이미지 찾기
                    img_tag = thumbnail_area.find("img") if thumbnail_area else None
                    img_src = urljoin(url, img_tag["src"]) if img_tag and img_tag.has_attr("src") else None

                    if href and img_src:
                        all_items.append({"페이지": page_num, "제목": title, "링크": href, "이미지": img_src})

    print(f"✅ 총 {len(all_items)}개의 블로그 글을 크롤링 완료!")
    return all_items

