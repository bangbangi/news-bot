import requests
import os
import json

def get_threads_token():
    username = os.environ["THREADS_USERNAME"]
    password = os.environ["THREADS_PASSWORD"]
    
    # Instagram Graph API로 토큰 발급
    url = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
    
    session = requests.Session()
    
    # 먼저 csrftoken 받기
    session.get("https://www.threads.net/")
    csrftoken = session.cookies.get("csrftoken", "")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrftoken,
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
        "Referer": "https://www.threads.net/",
    }
    
    data = {
        "username": username,
        "enc_password": f"#PWD_INSTAGRAM_BROWSER:0::{password}",
        "queryParams": "{}",
        "optIntoOneTap": "false",
    }
    
    response = session.post(url, headers=headers, data=data)
    result = response.json()
    
    if result.get("authenticated"):
        user_id = result.get("userId")
        return session, user_id
    else:
        raise Exception(f"로그인 실패: {result}")

def post_to_threads(text, image_path=None):
    username = os.environ["THREADS_USERNAME"]
    password = os.environ["THREADS_PASSWORD"]
    
    # Threads API 엔드포인트
    url = "https://graph.threads.net/v1.0"
    
    # 공식 API 대신 requests로 직접 포스팅
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Barcelona 289.0.0.77.109 Android",
    })
    
    # 로그인
    login_url = "https://i.instagram.com/api/v1/accounts/login/"
    login_data = {
        "username": username,
        "password": password,
        "device_id": "android-12345",
    }
    
    login_resp = session.post(login_url, data=login_data)
    login_json = login_resp.json()
    
    if "logged_in_user" not in login_json:
        raise Exception(f"로그인 실패: {login_json}")
    
    user_id = login_json["logged_in_user"]["pk"]
    print(f"로그인 성공: user_id={user_id}")
    
    # 텍스트 포스팅
    post_url = f"https://i.instagram.com/api/v1/media/configure_text_only_post/"
    post_data = {
        "publish_mode": "text_post",
        "text": text,
        "device_id": "android-12345",
    }
    
    post_resp = session.post(post_url, data=post_data)
    print(f"포스팅 결과: {post_resp.status_code}")
    print(post_resp.text[:500])

if __name__ == "__main__":
    with open("summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    post_to_threads(summary)