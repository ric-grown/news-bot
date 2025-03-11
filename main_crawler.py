import json
import random
import os
import requests
import base64
from blog_crawling import crawl_blog
from tistory import crawl_tistory
from enter_crawling import crawl_entertainment
from fashion_crawing import crawl_fashion
from news_crawling import crawl_news
from spots_crawling import crawl_sports

# 🔹 1️⃣ 이미지 URL을 Base64로 변환하는 함수
def convert_image_to_base64(image_url):
    try:
        response = requests.get(image_url, timeout=5)  # 이미지 요청
        if response.status_code == 200:
            return f"data:image/jpeg;base64,{base64.b64encode(response.content).decode('utf-8')}"
    except Exception as e:
        print(f"❌ 이미지 변환 실패: {image_url}, 오류: {e}")
    return image_url  # 변환 실패 시 원본 URL 유지

# 🔹 2️⃣ JSON 저장 함수
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 🔹 3️⃣ 데이터 크롤링 및 Base64 변환 적용
data_sources = {
    "blog_tistory": [],
    "entertainment": [],
    "fashion": [],
    "news": [],
    "sports": []
}

# 🔹 블로그 & 티스토리 크롤링
blog_data = crawl_blog()
tistory_data = crawl_tistory()
for item in blog_data + tistory_data:
    if "image" in item:
        item["image"] = convert_image_to_base64(item["image"])
data_sources["blog_tistory"].extend(blog_data + tistory_data)
save_json("blog_tistory.json", data_sources["blog_tistory"])

# 🔹 엔터테인먼트 크롤링
entertainment_data = crawl_entertainment()
with open("entertainment.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["entertainment"], f, ensure_ascii=False, indent=4)

# 🔹 패션 크롤링
fashion_data = crawl_fashion()
with open("fashion.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["fashion"], f, ensure_ascii=False, indent=4)

# 🔹 뉴스 크롤링
news_data = crawl_news()
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(data_sources["news"], f, ensure_ascii=False, indent=4)

# 🔹 스포츠 크롤링
sports_data = crawl_sports()
for item in sports_data:
    if "image" in item:
        item["image"] = convert_image_to_base64(item["image"])
data_sources["sports"].extend(sports_data)
save_json("sports.json", data_sources["sports"])

# 🔥 6️⃣ 모든 데이터를 합쳐서 랜덤 50개 추출 → `hotissue.json` 저장
all_data = (
    data_sources["blog_tistory"] +
    data_sources["entertainment"] +
    data_sources["fashion"] +
    data_sources["news"] +
    data_sources["sports"]
)

hot_issues = random.sample(all_data, min(50, len(all_data)))
save_json("hotissue.json", hot_issues)

print("✅ 모든 크롤링 및 이미지 변환 작업 완료! JSON 파일들이 저장되었습니다.")
