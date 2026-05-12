from datetime import datetime
import os

def make_html(summary_text):
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    # 국내/해외 섹션 분리
    domestic = ""
    global_news = ""
    
    lines = summary_text.split("\n")
    current = None
    for line in lines:
        if "🇰🇷" in line:
            current = "domestic"
        elif "🌏" in line:
            current = "global"
        elif current == "domestic" and line.strip():
            domestic += f"<p>{line}</p>"
        elif current == "global" and line.strip():
            global_news += f"<p>{line}</p>"

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    width: 900px;
    font-family: 'Noto Sans KR', sans-serif;
    background: #fffdf7;
  }}
  .card {{
    width: 900px;
    border: 3px solid #2a2a2a;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 6px 6px 0 #2a2a2a;
  }}
  .header {{
    background: #fffdf7;
    padding: 18px 24px 12px;
    text-align: center;
    border-bottom: 3px solid #2a2a2a;
  }}
  .header-date {{ font-size:15px; font-weight:700; color:#1a8a6e; letter-spacing:2px; }}
  .header-title {{ font-size:42px; font-weight:900; color:#1a1a1a; }}
  .header-title span {{ color:#1a8a6e; }}
  .body {{ display:grid; grid-template-columns:1fr 1fr; }}
  .section {{
    padding: 20px;
    border-right: 2px solid #2a2a2a;
  }}
  .section:last-child {{ border-right: none; }}
  .section-title {{
    font-size: 16px;
    font-weight: 900;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 2px solid #2a2a2a;
  }}
  .section p {{
    font-size: 13px;
    line-height: 1.7;
    color: #333;
    margin-bottom: 8px;
    padding-left: 8px;
    border-left: 3px solid #1a8a6e;
  }}
  .footer {{
    background: #1a8a6e;
    padding: 10px 24px;
    text-align: center;
    color: white;
    font-size: 13px;
    font-weight: 700;
  }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="header-date">☕ {today} 📰</div>
    <div class="header-title"><span>간추린</span> 아침뉴스</div>
  </div>
  <div class="body">
    <div class="section">
      <div class="section-title">🇰🇷 국내 뉴스</div>
      {domestic}
    </div>
    <div class="section">
      <div class="section-title">🌏 해외 뉴스</div>
      {global_news}
    </div>
  </div>
  <div class="footer">오늘의 이슈를 한눈에, 더 나은 하루를 위해! 🌟</div>
</div>
</body>
</html>"""
    
    with open("news_card.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("news_card.html 생성 완료")

if __name__ == "__main__":
    with open("summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    make_html(summary)