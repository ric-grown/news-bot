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

GITHUB_IMAGE_FOLDER = "images/"
GITHUB_REPO_URL = "https://raw.githubusercontent.com/ric-grown/news-bot/main/"  # GitHub Repo Raw URL

# 🔹 1️⃣ 기존 이미지 삭제 (폴더 초기화)
if os.path.exists(GITHUB_IMAGE_FOLDER):
    for file in os.listdir(GITHUB_IMAGE_FOLDER):
        file_path = os.path.join(GITHUB_IMAGE_FOLDER, file)
        os.remove(file_path)
else:
    os.makedirs(GITHUB_IMAGE_FOLDER)

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

# ✅ 이미지 다운로드 & 저장 함수
def download_and_save_image(image_url, filename):
    try:
        response = requests.get(image_url, timeout=5)
        if response.status_code == 200:
            with open(os.path.join(GITHUB_IMAGE_FOLDER, filename), "wb") as f:
                f.write(response.content)
            return f"{GITHUB_REPO_URL}{GITHUB_IMAGE_FOLDER}{filename}"
    except Exception as e:
        print(f"❌ 이미지 다운로드 실패: {image_url}, 오류: {e}")
    return None

# ✅ 크롤링 데이터 처리 & 이미지 저장
def process_crawled_data(crawled_data):
    updated_data = []
    for i, item in enumerate(crawled_data):
        if "image" in item:
            filename = f"{category}_{i}.jpg"
            image_url = download_and_save_image(item["image"], filename)
            if image_url:
                item["image"] = image_url
        updated_data.append(item)
    return updated_data

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
data_sources["blog_tistory"].extend(blog_data + tistory_data)
data_sources["blog_tistory"] = process_crawled_data(data_sources["blog_tistory"])
save_json("blog_tistory.json", data_sources["blog_tistory"])

# 🔹 엔터테인먼트 크롤링
entertainment_data = crawl_entertainment()
data_sources["entertainment"].extend(entertainment_data)
save_json("entertainment.json", data_sources["entertainment"])

# 🔹 패션 크롤링
fashion_data = crawl_fashion()
data_sources["fashion"].extend(fashion_data)
save_json("fashion.json", data_sources["fashion"])

# 🔹 뉴스 크롤링
news_data = crawl_news()
data_sources["news"].extend(news_data)
save_json("news.json", data_sources["news"])

# 🔹 스포츠 크롤링
sports_data = crawl_sports()
data_sources["sports"].extend(sports_data)
data_sources["sports"] = process_crawled_data(data_sources["sports"])
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
