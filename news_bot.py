import feedparser
import anthropic

# 1) 뉴스 수집
def fetch_news():
    feeds = [
        "https://www.hankyung.com/feed/all-news",
        "https://www.mk.co.kr/rss/30000001/",
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

# 2) Claude로 요약
def summarize(articles):
    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 자동 참조
    text = "\n".join([f"- {a['title']}" for a in articles])
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": f"다음 뉴스를 Threads용으로 요약:\n{text}"}]
    )
    return msg.content[0].text

if __name__ == "__main__":
    articles = fetch_news()
    result = summarize(articles)
    print(result)
