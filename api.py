import requests

BASE_URL = "http://192.168.1.51:5000"


def get_comments(news_id):
    try:
        response = requests.get(f"{BASE_URL}/comments/{news_id}")
        return response.json()
    except Exception as e:
        print("[ERROR] get_comments:", e)
        return []


def add_comment(news_id, user_login, text):
    try:
        payload = {"news_id": news_id, "user_login": user_login, "text": text}
        requests.post(f"{BASE_URL}/comments", json=payload)
    except Exception as e:
        print("[ERROR] add_comment:", e)


def get_chat():
    try:
        response = requests.get(f"{BASE_URL}/chat")
        return response.json()
    except Exception as e:
        print("[ERROR] get_chat:", e)
        return []


def send_message(login, message):
    try:
        payload = {"login": login, "message": message}
        requests.post(f"{BASE_URL}/chat", json=payload)
    except Exception as e:
        print("[ERROR] send_message:", e)


def check_user(username, password):
    try:
        response = requests.post(f"{BASE_URL}/check_user", json={"login": username, "password": password})
        return response.json().get("valid", False)
    except Exception as e:
        print("[ERROR] check_user:", e)
        return False


def get_user_role(username):
    try:
        response = requests.get(f"{BASE_URL}/user_role/{username}")
        return response.json().get("role", "студент")
    except Exception as e:
        print("[ERROR] get_user_role:", e)
        return "студент"


def register_user(username, password, role):
    try:
        response = requests.post(f"{BASE_URL}/register", json={
            "login": username,
            "password": password,
            "role": role
        })
        return response.status_code == 200
    except Exception as e:
        print("[ERROR] register_user:", e)
        return False


def add_like(news_id, user_login):
    try:
        requests.post(f"{BASE_URL}/like", json={"news_id": news_id, "user_login": user_login})
    except Exception as e:
        print("[ERROR] add_like:", e)


def count_likes(news_id):
    try:
        r = requests.get(f"{BASE_URL}/like/{news_id}")
        return r.json().get("count", 0)
    except Exception as e:
        print("[ERROR] count_likes:", e)
        return 0


def add_specialty_like(specialty_id, user_login):
    try:
        requests.post(f"{BASE_URL}/specialty_like", json={"specialty_id": specialty_id, "user_login": user_login})
    except Exception as e:
        print("[ERROR] add_specialty_like:", e)


def count_specialty_likes(specialty_id):
    try:
        r = requests.get(f"{BASE_URL}/specialty_like/{specialty_id}")
        return r.json().get("count", 0)
    except Exception as e:
        print("[ERROR] count_specialty_likes:", e)
        return 0

def upload_news(title, content, image_path, external_link):
    try:
        response = requests.post(f"{BASE_URL}/news", json={
            "title": title,
            "content": content,
            "image_path": image_path,
            "external_link": external_link
        })
        return response.status_code == 200
    except Exception as e:
        print("[ERROR] upload_news:", e)
        return False


def get_all_news():
    try:
        r = requests.get(f"{BASE_URL}/news")
        return r.json()
    except Exception as e:
        print("[ERROR] get_all_news:", e)
        return []


def get_all_specialties():
    try:
        r = requests.get(f"{BASE_URL}/specialties")
        return r.json()  # теперь вернёт список словарей с id
    except Exception as e:
        print("[ERROR] get_all_specialties:", e)
        return []
