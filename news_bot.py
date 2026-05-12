import feedparser
import anthropic
import os

def fetch_news():
    feeds = [
        "https://www.hankyung.com/feed/all-news",
        "https://www.mk.co.kr/rss/30000001/",
        "https://rss.etnews.com/Section901.xml",
    ]
    articles = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            articles.append({
                "title": entry.title,
                "summary": entry.get("summary", "")[:200]
            })
    return articles

def summarize(articles):
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    text = "\n".join([f"- {a['title']}" for a in articles])
    
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": f"""다음 뉴스 기사들을 Threads 게시용으로 요약해줘.

{text}

형식:
📰 오늘의 주요 뉴스

- 핵심 기사 5개를 2줄씩 요약
- 마지막에 해시태그 5개
"""
        }]
    )
    return msg.content[0].text

if __name__ == "__main__":
    print("뉴스 수집 중...")
    articles = fetch_news()
    print(f"기사 {len(articles)}개 수집 완료")
    
    print("Claude 요약 중...")
    result = summarize(articles)
    print("\n=== 결과 ===")
    print(result)
