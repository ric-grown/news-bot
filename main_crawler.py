import json
import random
import os
from blog_crawling import crawl_blog
from tistory import crawl_tistory
from enter_crawling import crawl_entertainment
from fashion_crawing import crawl_fashion
from news_crawling import crawl_news
from spots_crawling import crawl_sports

# 개별 JSON 파일에 저장할 데이터
data_sources = {
    "blog_tistory": [],
    "entertainment": [],
    "fashion": [],
    "news": [],
    "sports": []
}

# 🔹 1️⃣ 블로그 & 티스토리 크롤링 → 한 개의 JSON 파일로 저장
blog_data = crawl_blog()
tistory_data = crawl_tistory()
data_sources["blog_tistory"].extend(blog_data + tistory_data)

with open("blog_tistory.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["blog_tistory"], f, ensure_ascii=False, indent=4)

# 🔹 2️⃣ 엔터테인먼트 크롤링
entertainment_data = crawl_entertainment()
data_sources["entertainment"].extend(entertainment_data)

with open("entertainment.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["entertainment"], f, ensure_ascii=False, indent=4)

# 🔹 3️⃣ 패션 크롤링
fashion_data = crawl_fashion()
data_sources["fashion"].extend(fashion_data)

with open("fashion.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["fashion"], f, ensure_ascii=False, indent=4)

# 🔹 4️⃣ 뉴스 크롤링
news_data = crawl_news()
data_sources["news"].extend(news_data)

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["news"], f, ensure_ascii=False, indent=4)

# 🔹 5️⃣ 스포츠 크롤링
sports_data = crawl_sports()
data_sources["sports"].extend(sports_data)

with open("sports.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["sports"], f, ensure_ascii=False, indent=4)

# 🔥 6️⃣ 모든 데이터를 합쳐서 랜덤 50개 추출 → `hotissue.json` 저장
all_data = (
    data_sources["blog_tistory"] +
    data_sources["entertainment"] +
    data_sources["fashion"] +
    data_sources["news"] +
    data_sources["sports"]
)

hot_issues = random.sample(all_data, min(50, len(all_data)))

with open("hotissue.json", "w", encoding="utf-8") as f:
    json.dump(hot_issues, f, ensure_ascii=False, indent=4)

print("✅ 모든 크롤링 작업 완료! JSON 파일들이 저장되었습니다.")
