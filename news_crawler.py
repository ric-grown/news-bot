import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# JSON 파일 저장 함수
def save_to_json(data, filename="now_news.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ 데이터 저장 완료: {filename}")

# 🔍 1. 네이버 뉴스 크롤링
# 🔍 1. 네이버 뉴스 크롤링 (이미지 밀림 문제 해결)
def get_naver_news():
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    news_list = []
    news_items = soup.select(".rankingnews_box .list_content li")[:10]  # 각 뉴스 리스트 항목 선택

    for item in news_items:
        try:
            link_tag = item.find("a")  # 뉴스 링크
            title = link_tag.text.strip() if link_tag else "제목 없음"
            link = "https://news.naver.com" + link_tag["href"] if link_tag and link_tag["href"].startswith("/") else link_tag["href"]

            # 뉴스 항목 내부에서 직접 이미지 가져오기
            image_tag = item.find("img")
            image = image_tag["src"] if image_tag else "https://via.placeholder.com/150"

            news_list.append({"title": title, "link": link, "image": image, "source": "네이버 뉴스"})
        except Exception as e:
            print(f"❌ 네이버 뉴스 크롤링 오류: {e}")
            continue
    
    print("✔ 네이버 뉴스 크롤링 완료.")
    return news_list

# 🔍 2. 네이버 인기 블로그 크롤링
def get_naver_blogs():
    url = "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.hot_topic")))
    
    blog_list = []
    blog_elements = driver.find_elements(By.CSS_SELECTOR, "section.hot_topic .list_hottopic .item")[:5]
    
    for blog in blog_elements:
        try:
            title = blog.find_element(By.CSS_SELECTOR, ".title_post").text.strip()
            link = blog.find_element(By.CSS_SELECTOR, "a.item_inner").get_attribute("href")
            image = blog.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            blog_list.append({"title": title, "link": link, "image": image, "source": "네이버 블로그"})
        except:
            continue
    
    driver.quit()
    print("✔ 네이버 블로그 크롤링 완료.")
    return blog_list

# 🔍 3. 티스토리 인기 블로그 크롤링
def get_tistory_blogs():
    url = "https://www.tistory.com/category/ranking"
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cont_g")))
    
    tistory_list = []
    post_elements = driver.find_elements(By.CSS_SELECTOR, "div.cont_g")[:5]
    
    for post in post_elements:
        try:
            title = post.find_element(By.CSS_SELECTOR, "strong.tit_g").text.strip()
            link = post.find_element(By.CSS_SELECTOR, "a.link_cont.zoom_cont").get_attribute("href")
            image = post.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            tistory_list.append({"title": title, "link": link, "image": image, "source": "티스토리"})
        except:
            continue
    
    driver.quit()
    print("✔ 티스토리 블로그 크롤링 완료.")
    return tistory_list

# 🔄 전체 실행
def main():
    print("🚀 데이터 수집 시작...")
    naver_news = get_naver_news()
    naver_blogs = get_naver_blogs()
    tistory_blogs = get_tistory_blogs()
    
    all_data = naver_news + naver_blogs + tistory_blogs
    save_to_json(all_data)
    print("🎉 모든 크롤링 완료!")

if __name__ == "__main__":
    main()
