import requests
from bs4 import BeautifulSoup

def get_naver_news(query="경제 뉴스", max_results=5):
    search_url = f"https://search.naver.com/search.naver?where=news&query=경제 뉴스"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    news_items = []
    results = soup.find_all("a", class_="news_tit")[:max_results]  # 상위 max_results개만 가져오기

    for result in results:
        title = result.text
        link = result["href"]
        news_items.append((title, link))

    return news_items

# 실행 예시
news_list = get_naver_news()
for i, (title, link) in enumerate(news_list, 1):
    print(f"{i}. {title} - {link}")
