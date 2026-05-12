import os
import subprocess
from pathlib import Path

from image_uploader import can_upload_images, upload_images
from make_card import make_html, make_individual_html
from news_bot import fetch_news, save_summary, summarize
from threads_post import post_carousel_to_threads


def render_png(input_html, output_png):
    subprocess.run(
        ["node", "screenshot.js", input_html, output_png],
        check=True,
    )
    return output_png


def build_images(summary, mode):
    if mode == "carousel":
        html_files = make_individual_html(summary)
        return [
            render_png(html_file, str(Path(html_file).with_suffix(".png")))
            for html_file in html_files
        ]

    make_html(summary, "news_card.html")
    return [render_png("news_card.html", "news_card.png")]


def configured_image_urls():
    raw = os.getenv("THREADS_IMAGE_URLS") or os.getenv("THREADS_IMAGE_URL") or ""
    return [url.strip() for url in raw.split(",") if url.strip()]


def main():
    mode = os.getenv("IMAGE_MODE", "combined").lower()
    if mode not in ("combined", "carousel"):
        raise ValueError("IMAGE_MODE는 combined 또는 carousel만 지원합니다.")

    print("뉴스 수집 중...")
    articles = fetch_news()
    print(f"기사 {len(articles)}개 수집 완료")

    print("Gemini 요약 중...")
    summary = summarize(articles)
    save_summary(summary)

    print(f"이미지 생성 중... mode={mode}")
    image_paths = build_images(summary, mode)

    image_urls = configured_image_urls()
    if not image_urls and can_upload_images():
        image_urls = upload_images(image_paths)

    if not image_urls:
        print("공개 이미지 URL 또는 Cloudinary 설정이 없어 텍스트만 게시합니다.")

    post_carousel_to_threads(summary, image_urls)


if __name__ == "__main__":
    main()
