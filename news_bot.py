import feedparser
from google import genai
import os

def fetch_news():
    feeds = {
        "한국경제": "https://www.hankyung.com/feed/all-news",
        "매일경제": "https://www.mk.co.kr/rss/30000001/",
        "전자신문": "https://rss.etnews.com/Section901.xml",
        "연합뉴스": "https://www.yonhapnewstv.co.kr/feed/",
        "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "Bloomberg": "https://feeds.bloomberg.com/markets/news.rss",
        "Reuters": "https://feeds.reuters.com/reuters/businessNews",
        "Financial Times": "https://www.ft.com/rss/home",
        "CNBC": "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    }
    articles = []
    for source, url in feeds.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                articles.append({
                    "source": source,
                    "title": entry.title,
                    "summary": entry.get("summary", "")[:300]
                })
        except Exception as e:
            print(f"{source} 수집 실패: {e}")
    return articles

def summarize(articles):
    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"],
        http_options={"api_version": "v1alpha"}
    )
    text = "\n".join([f"[{a['source']}] {a['title']}" for a in articles])

    prompt = f"""다음은 한국 및 해외 주요 언론사의 뉴스입니다. 해외 기사는 한국어로 번역해서 요약해줘.

{text}

아래 형식으로 작성해줘:

📰 오늘의 주요 뉴스 (날짜)

🇰🇷 국내
- 기사 제목 요약 (출캘)
  핵심 내용 1~2줄

🌏 해외
- 기사 제목 요약 (출캘)
  핵심 내용 1~2줄 (한국어 번역)

#해시태그 5개
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def save_summary(result):
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(result)
    print("summary.txt 저장 완료")

if __name__ == "__main__":
    print("뉴스 수집 중...")
    articles = fetch_news()
    print(f"기사 {len(articles)}개 수집 완료")
    print("Gemini 요약 중...")
    result = summarize(articles)
    print("\n=== 결과 ===")
    print(result)
    save_summary(result)
