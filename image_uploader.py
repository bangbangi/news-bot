import hashlib
import os
import time

import requests


def _cloudinary_configured():
    return bool(os.getenv("CLOUDINARY_CLOUD_NAME")) and (
        bool(os.getenv("CLOUDINARY_UPLOAD_PRESET"))
        or (bool(os.getenv("CLOUDINARY_API_KEY")) and bool(os.getenv("CLOUDINARY_API_SECRET")))
    )


def upload_to_cloudinary(image_path):
    """Upload a local PNG/JPG to Cloudinary and return a public HTTPS URL."""
    if not _cloudinary_configured():
        raise RuntimeError(
            "Cloudinary 환경변수가 없습니다. CLOUDINARY_CLOUD_NAME과 "
            "CLOUDINARY_UPLOAD_PRESET 또는 CLOUDINARY_API_KEY/CLOUDINARY_API_SECRET을 설정하세요."
        )

    cloud_name = os.environ["CLOUDINARY_CLOUD_NAME"]
    upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
    folder = os.getenv("CLOUDINARY_FOLDER", "threads-news-bot")

    data = {"folder": folder}
    if os.getenv("CLOUDINARY_UPLOAD_PRESET"):
        data["upload_preset"] = os.environ["CLOUDINARY_UPLOAD_PRESET"]
    else:
        timestamp = str(int(time.time()))
        data.update(
            {
                "api_key": os.environ["CLOUDINARY_API_KEY"],
                "timestamp": timestamp,
            }
        )
        signature_base = "&".join(f"{key}={data[key]}" for key in sorted(data))
        data["signature"] = hashlib.sha1(
            f"{signature_base}{os.environ['CLOUDINARY_API_SECRET']}".encode("utf-8")
        ).hexdigest()

    with open(image_path, "rb") as image_file:
        response = requests.post(
            upload_url,
            data=data,
            files={"file": image_file},
            timeout=120,
        )

    payload = response.json()
    if "secure_url" not in payload:
        raise RuntimeError(f"Cloudinary 업로드 실패: {payload}")

    print(f"이미지 업로드 완료: {payload['secure_url']}")
    return payload["secure_url"]


def upload_images(image_paths):
    return [upload_to_cloudinary(path) for path in image_paths]


def can_upload_images():
    return _cloudinary_configured()
