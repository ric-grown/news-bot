import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import openai
from datetime import datetime
from bs4 import BeautifulSoup
from notion_client import Client

# API 키 설정
NOTION_API_KEY = "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"
DATABASE_ID = "1a8d4354-89e3-80f9-9373-cef0f33be8fe"
OPENAI_API_KEY = "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"

# Notion API 설정
notion = Client(auth=NOTION_API_KEY)

# 🔍 1. 네이버 실시간 인기 뉴스 크롤링
def get_naver_trending_news():
    url = "https://news.naver.com/main/ranking/popularDay.naver"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    trending_news = []
    
    results = soup.select(".rankingnews_box .list_content a")[:10]
    for result in results:
        title = result.text.strip()
        link = "https://news.naver.com" + result["href"] if result["href"].startswith("/") else result["href"]
        trending_news.append((title, link))
        
    print("뉴스 탐색 완료.")

    return trending_news

# 🔍 2. 네이버 인기 블로그 크롤링 (방문자 수 기준)
def get_naver_hot_topic_blogs():
    url = "https://section.blog.naver.com/BlogHome.naver?directoryNo=0&currentPage=1&groupId=0"

    options = Options()
    options.add_argument("--headless")  # 브라우저를 띄우지 않고 실행

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.hot_topic")))

    trending_blogs = []
    blog_elements = driver.find_elements(By.CSS_SELECTOR, "section.hot_topic .list_hottopic .item")[:3]

    for blog in blog_elements:
        try:
            title = blog.find_element(By.CSS_SELECTOR, ".title_post").text.strip()
            link = blog.find_element(By.CSS_SELECTOR, "a.item_inner").get_attribute("href")
            trending_blogs.append((title, link))
        except:
            continue
    
    print("블로그 탐색 완료.")
    
    driver.quit()
    return trending_blogs

# 🔍 3. 티스토리 인기 블로그 크롤링
def get_tistory_trending_selenium():
    options = Options()
    options.add_argument("--headless")  # 창을 띄우지 않고 실행

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.tistory.com/category/ranking")

    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.cont_g")))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    post_elements = driver.find_elements(By.CSS_SELECTOR, "div.cont_g")[:10]
    trending_tistory = []

    for post in post_elements:
        try:
            post_title = post.find_element(By.CSS_SELECTOR, "strong.tit_g").text.strip()
            post_url = post.find_element(By.CSS_SELECTOR, "a.link_cont.zoom_cont").get_attribute("href")
            trending_tistory.append((post_title, post_url))
        except:
            continue
        
    print("티스토리 탐색 완료.")    
        
    driver.quit()
    return trending_tistory

# 🔥 4. GPT-4 API를 이용해 블로그 & 쇼츠 주제 추천
def generate_topics(search_trends):
    client = openai.Client(api_key=OPENAI_API_KEY)
    prompt = f"""
    최근 검색 트렌드 {search_trends}를 참고하여,
    - 블로그 주제 3개
    - 쇼츠 주제 3개
    를 추천해줘.

    참고 데이터:  
    네이버 뉴스 인기 기사:  
    - 기사 제목과 내용을 분석하여 **사회적, 경제적, 기술적, 문화적 영향**을 고려한 새로운 인사이트를 도출하세요.  
    - 예를 들어, 국민연금 손실 뉴스가 있다면 **"국민연금과 대기업의 위험한 관계"**, **"연금을 대신할 투자 전략"** 등  
        보다 깊이 있는 논의가 가능한 주제를 도출합니다.  

    네이버 블로그 핫토픽:  
    - 현재 인기 있는 레시피, 라이프스타일, 생활 정보 콘텐츠를 분석하여  
        **단순한 레시피 소개가 아닌, 사람들이 이런 콘텐츠를 찾는 심리적/사회적 이유**를 분석한 주제를 제시하세요.  
    - 예를 들어, **"집밥 열풍의 진짜 이유 - 한국인의 외식 문화 변화"**, **"건강식 트렌드가 우리 식생활을 바꾸는 법"** 같은  
        **트렌드의 본질을 다루는 주제**를 생각해보세요.  

    티스토리 인기 블로그:  
    - 최신 IT, 경제, 리뷰 콘텐츠를 활용하여 사람들이 **단순히 제품 리뷰를 넘어, 트렌드 변화를 이해할 수 있는 주제**를 도출하세요.  
    - 예를 들어, **"햄버거 가격이 점점 오르는 이유 - 패스트푸드 업계의 경제학"**,  
        **"전기차 디자인이 변화하는 이유 - 소비자 심리 분석"** 등,  
        **제품 이면에 숨겨진 트렌드와 산업 변화**를 주제로 삼을 수 있습니다.  
     
    각 주제에 대해 다음 정보를 포함해줘:
    - 카테고리 (해당 주제가 속하는 분야, 예: 경제, 투자, 라이프스타일, 테크 등)
    - 추천 키워드 3개 (SEO 최적화를 고려한 핵심 키워드)
    - 블로그 글 작성 프롬프트 (해당 주제에 대해 블로그 글을 작성할 때 활용할 가이드)
    - 쇼츠 내용 작성 프롬프트 (쇼츠를 제작할 때 사용할 가이드)

    출력 형식 예시:
    [블로그 주제] "주제 제목"
    카테고리: [카테고리명]
    추천 키워드: #키워드1 #키워드2 #키워드3
    블로그 글 작성 프롬프트: "..."

    [쇼츠 주제] "주제 제목"
    카테고리: [카테고리명]
    추천 키워드: #키워드1 #키워드2 #키워드3
    쇼츠 내용 작성 프롬프트: "..."
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an expert content strategist specializing in blog and short-form video topics."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    topics = response.choices[0].message.content.split("\n")

    blog_topics = []
    shorts_topics = []

    current_category = None
    current_keywords = None
    current_prompt = None

    for i, t in enumerate(topics):
        t = t.strip()
        if t.startswith("[블로그 주제]"):
            if current_category and current_keywords and current_prompt:
                blog_topics.append((blog_title, current_category, current_keywords, current_prompt))
            blog_title = t.replace("[블로그 주제]", "").strip()
            current_category = None
            current_keywords = None
            current_prompt = None

        elif t.startswith("[쇼츠 주제]"):
            if current_category and current_keywords and current_prompt:
                shorts_topics.append((shorts_title, current_category, current_keywords, current_prompt))
            shorts_title = t.replace("[쇼츠 주제]", "").strip()
            current_category = None
            current_keywords = None
            current_prompt = None

        elif t.startswith("카테고리:"):
            current_category = t.replace("카테고리:", "").strip()
        
        elif t.startswith("키워드:"):
            current_keywords = t.replace("키워드:", "").strip()

        elif t.startswith("블로그 프롬프트:"):
            current_prompt = t.replace("블로그 프롬프트:", "").strip()

        elif t.startswith("쇼츠 프롬프트:"):
            current_prompt = t.replace("쇼츠 프롬프트:", "").strip()

    # 마지막 항목 추가
    if current_category and current_keywords and current_prompt:
        if len(blog_topics) < 3:
            blog_topics.append((blog_title, current_category, current_keywords, current_prompt))
        else:
            shorts_topics.append((shorts_title, current_category, current_keywords, current_prompt))

    return blog_topics, shorts_topics


# 📝 5. Notion에 데이터 추가
def add_topic_to_notion(category, title, source, keywords):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "날짜": {"date": {"start": datetime.today().strftime("%Y-%m-%d")}},
            "카테고리": {"select": {"name": category}},
            "이름": {
                "title": [{"type": "text", "text": {"content": title, "link": None}}]
            },
            "참고 내용": {"rich_text": [{"text": {"content": source}}]},
            "추천 키워드": {"multi_select": [{"name": kw} for kw in keywords]},
            "작성 상태": {"select": {"name": "초안"}},
        }
    }
    try:
        notion.pages.create(**data)
        print(f"✅ Notion에 추가됨: {title}")
    except Exception as e:
        print(f"❌ Notion API 에러: {e}")

# 🔄 6. 전체 실행 프로세스
def main():
    # 최신 검색 트렌드 가져오기 (네이버 뉴스 + 네이버 인기 블로그 + 티스토리 인기 블로그)
    naver_news = get_naver_trending_news()
    naver_blogs = get_naver_hot_topic_blogs()
    tistory_blogs = get_tistory_trending_selenium()
    
    search_trends = list(set(naver_news+naver_blogs+tistory_blogs))
    # generate_topics 실행
    blog_topics, shorts_topics = generate_topics(search_trends)

    # Notion에 블로그 주제 추가
    for topic in blog_topics:
        title, category, keywords, source = topic  
        add_topic_to_notion(category, title, source, keywords)

    # Notion에 쇼츠 주제 추가
    for topic in shorts_topics:
        title, category, keywords, source = topic  
        add_topic_to_notion(category, title, source, keywords)
    
if __name__ == "__main__":
    main()
