from datetime import datetime
from notion_client import Client

# Notion API 설정
NOTION_SECRET = "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"
DATABASE_ID = "1a8d4354-89e3-80f9-9373-cef0f33be8fe"
notion = Client(auth=NOTION_SECRET)

# 블로그 주제 생성 (GPT-4 API 사용)

# Notion에 데이터 추가하는 함수 (notion_client 사용)
def add_topic_to_notion(category, title, source, keywords):
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "날짜": {"date": {"start": datetime.today().strftime("%Y-%m-%d")}},
            "카테고리": {"select": {"name": category}},
            "주제 제목": {"title": [{"text": {"content": title}}]},
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

# 실행 예제
add_topic_to_notion("경제", "topic", "aaaaaaa", ["경제", "트렌드"])

