import requests
import os
import time


def post_to_threads(text, image_path=None):
        access_token = os.environ["THREADS_ACCESS_TOKEN"]
        user_id = os.environ["THREADS_USER_ID"]

    base_url = "https://graph.threads.net/v1.0"

    # 1단계: 미디어 컨테이너 생성
    create_url = f"{base_url}/{user_id}/threads"

    if image_path:
                # 이미지가 있는 경우 (image_url은 공개 URL이어야 함)
                create_params = {
                                "media_type": "IMAGE",
                                "image_url": image_path,
                                "text": text,
                                "access_token": access_token,
                }
else:
            create_params = {
                            "media_type": "TEXT",
                            "text": text,
                            "access_token": access_token,
            }

    create_resp = requests.post(create_url, params=create_params)
    create_json = create_resp.json()
    print(f"컨테이너 생성 결과: {create_json}")

    if "id" not in create_json:
                raise Exception(f"컨테이너 생성 실패: {create_json}")

    container_id = create_json["id"]

    # 잠시 대기 (Meta 권장)
    time.sleep(3)

    # 2단계: 게시
    publish_url = f"{base_url}/{user_id}/threads_publish"
    publish_params = {
                "creation_id": container_id,
                "access_token": access_token,
    }

    publish_resp = requests.post(publish_url, params=publish_params)
    publish_json = publish_resp.json()
    print(f"포스팅 결과: {publish_json}")

    if "id" not in publish_json:
                raise Exception(f"포스팅 실패: {publish_json}")

    print(f"포스팅 성공! Thread ID: {publish_json['id']}")
    return publish_json["id"]


if __name__ == "__main__":
        with open("summary.txt", "r", encoding="utf-8") as f:
                    summary = f.read()
                post_to_threads(summary)
