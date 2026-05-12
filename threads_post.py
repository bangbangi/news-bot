import requests
import os
import time
from urllib.parse import urlparse


def get_user_id(access_token):
    """액세스 토큰으로 Threads User ID 자동 조회"""
    resp = requests.get(
        "https://graph.threads.net/v1.0/me",
        params={"fields": "id,username", "access_token": access_token}
    )
    data = resp.json()
    if "id" not in data:
        raise Exception(f"User ID 조회 실패: {data}")
    print(f"Threads 계정: @{data.get('username')} (id: {data['id']})")
    return data["id"]


def trim_text(text):
    # Threads API 최대 500자 제한
    MAX_LEN = 500
    if len(text) > MAX_LEN:
        text = text[:MAX_LEN - 1] + "…"
    print(f"포스팅 텍스트 길이: {len(text)}자")
    return text


def validate_public_image_url(image_url):
    parsed = urlparse(image_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError(
            "Threads 이미지 업로드에는 로컬 파일 경로가 아니라 공개 image_url이 필요합니다."
        )


def create_container(user_id, access_token, params):
    create_url = f"https://graph.threads.net/v1.0/{user_id}/threads"
    create_resp = requests.post(
        create_url,
        params={**params, "access_token": access_token},
        timeout=60,
    )
    create_json = create_resp.json()
    print(f"컨테이너 생성 결과: {create_json}")

    if "id" not in create_json:
        raise Exception(f"컨테이너 생성 실패: {create_json}")
    return create_json["id"]


def publish_container(user_id, access_token, container_id):
    wait_seconds = int(os.getenv("THREADS_PUBLISH_WAIT_SECONDS", "30"))
    print(f"게시 전 {wait_seconds}초 대기 중...")
    time.sleep(wait_seconds)

    publish_url = f"https://graph.threads.net/v1.0/{user_id}/threads_publish"
    publish_resp = requests.post(
        publish_url,
        params={
            "creation_id": container_id,
            "access_token": access_token,
        },
        timeout=60,
    )
    publish_json = publish_resp.json()
    print(f"포스팅 결과: {publish_json}")

    if "id" not in publish_json:
        raise Exception(f"포스팅 실패: {publish_json}")

    print(f"포스팅 성공! Thread ID: {publish_json['id']}")
    return publish_json["id"]


def post_to_threads(text, image_url=None):
    access_token = os.environ["THREADS_ACCESS_TOKEN"]
    user_id = get_user_id(access_token)
    text = trim_text(text)

    if image_url:
        validate_public_image_url(image_url)
        params = {
            "media_type": "IMAGE",
            "image_url": image_url,
            "text": text,
        }
    else:
        params = {
            "media_type": "TEXT",
            "text": text,
        }

    container_id = create_container(user_id, access_token, params)
    return publish_container(user_id, access_token, container_id)


def post_carousel_to_threads(text, image_urls):
    if not image_urls:
        return post_to_threads(text)
    if len(image_urls) == 1:
        return post_to_threads(text, image_urls[0])

    access_token = os.environ["THREADS_ACCESS_TOKEN"]
    user_id = get_user_id(access_token)
    text = trim_text(text)

    child_ids = []
    for image_url in image_urls[:20]:
        validate_public_image_url(image_url)
        child_id = create_container(
            user_id,
            access_token,
            {
                "media_type": "IMAGE",
                "image_url": image_url,
                "is_carousel_item": "true",
            },
        )
        child_ids.append(child_id)

    parent_id = create_container(
        user_id,
        access_token,
        {
            "media_type": "CAROUSEL",
            "children": ",".join(child_ids),
            "text": text,
        },
    )
    return publish_container(user_id, access_token, parent_id)


def env_image_urls():
    raw = os.getenv("THREADS_IMAGE_URLS") or os.getenv("THREADS_IMAGE_URL") or ""
    return [url.strip() for url in raw.split(",") if url.strip()]


if __name__ == "__main__":
    with open("summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    urls = env_image_urls()
    post_carousel_to_threads(summary, urls)
