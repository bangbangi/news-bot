from datetime import datetime
from html import escape
from pathlib import Path


def parse_summary_sections(summary_text):
    sections = {"domestic": [], "global": []}
    current = None
    current_item = None

    for raw_line in summary_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "🇰🇷" in line:
            current = "domestic"
            current_item = None
            continue
        if "🌏" in line:
            current = "global"
            current_item = None
            continue
        if current not in sections or line.startswith("#"):
            continue

        if line.startswith("-"):
            current_item = {"title": line.lstrip("- ").strip(), "details": []}
            sections[current].append(current_item)
        elif current_item:
            current_item["details"].append(line)
        else:
            sections[current].append({"title": line, "details": []})

    return sections


def _render_items(items):
    if not items:
        return "<p>수집된 뉴스가 없습니다.</p>"

    html = []
    for item in items:
        title = escape(item["title"])
        details = " ".join(item.get("details", []))
        detail_html = f"<span>{escape(details)}</span>" if details else ""
        html.append(f"<p><strong>{title}</strong>{detail_html}</p>")
    return "\n".join(html)


def make_html(summary_text, output_path="news_card.html"):
    today = datetime.now().strftime("%Y년 %m월 %d일")
    sections = parse_summary_sections(summary_text)
    domestic = _render_items(sections["domestic"])
    global_news = _render_items(sections["global"])

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
  .section p strong {{
    display: block;
    font-size: 14px;
    color: #111;
    margin-bottom: 2px;
  }}
  .section p span {{
    display: block;
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

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{output_path} 생성 완료")


def make_individual_html(summary_text, output_dir="cards"):
    today = datetime.now().strftime("%Y년 %m월 %d일")
    sections = parse_summary_sections(summary_text)
    output = Path(output_dir)
    output.mkdir(exist_ok=True)
    files = []

    all_items = []
    for section_key, section_name in (("domestic", "국내 뉴스"), ("global", "해외 뉴스")):
        for item in sections[section_key]:
            all_items.append((section_name, item))

    for index, (section_name, item) in enumerate(all_items, start=1):
        details = " ".join(item.get("details", []))
        html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    width: 900px;
    min-height: 900px;
    font-family: 'Noto Sans KR', sans-serif;
    background: #fffdf7;
    padding: 28px;
  }}
  .card {{
    width: 844px;
    min-height: 844px;
    border: 3px solid #2a2a2a;
    border-radius: 16px;
    box-shadow: 7px 7px 0 #2a2a2a;
    padding: 42px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}
  .meta {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 18px;
    font-weight: 900;
    color: #1a8a6e;
  }}
  .label {{
    border: 2px solid #1a8a6e;
    border-radius: 999px;
    padding: 8px 16px;
  }}
  .title {{
    margin-top: 58px;
    font-size: 50px;
    line-height: 1.22;
    font-weight: 900;
    color: #111;
    word-break: keep-all;
  }}
  .detail {{
    margin-top: 34px;
    font-size: 27px;
    line-height: 1.58;
    font-weight: 700;
    color: #333;
    word-break: keep-all;
  }}
  .footer {{
    border-top: 3px solid #2a2a2a;
    padding-top: 18px;
    display: flex;
    justify-content: space-between;
    color: #555;
    font-size: 17px;
    font-weight: 700;
  }}
</style>
</head>
<body>
  <div class="card">
    <div>
      <div class="meta">
        <span>{escape(today)}</span>
        <span class="label">{escape(section_name)}</span>
      </div>
      <div class="title">{escape(item["title"])}</div>
      <div class="detail">{escape(details)}</div>
    </div>
    <div class="footer">
      <span>간추린 아침뉴스</span>
      <span>{index:02d}</span>
    </div>
  </div>
</body>
</html>"""
        file_path = output / f"news_card_{index:02d}.html"
        file_path.write_text(html, encoding="utf-8")
        files.append(str(file_path))

    print(f"개별 카드 HTML {len(files)}개 생성 완료")
    return files

if __name__ == "__main__":
    with open("summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    make_html(summary)
