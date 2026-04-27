import requests
import time
from config import ACCESS_TOKEN, PAGE_ID

def post_to_facebook(image_url, caption):
    url = f'https://graph.facebook.com/v25.0/{PAGE_ID}/photos'

    payload = {
        'caption': caption,
        'access_token': ACCESS_TOKEN,
    }

    files = {
        'source': open(image_url, 'rb')
    }

    response = requests.post(url, data=payload, files=files)
    result = response.json()

    if "error" in result:
        raise Exception(result["error"])

    return result

def check_post_if_error(caption, retries=10, delay=2):
    url = f'https://graph.facebook.com/v25.0/{PAGE_ID}/feed'

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'message',
        'limit': 10  # recent posts only
    }

    for _ in range(retries):
        response = requests.get(url, params=params)
        result = response.json()

        if "error" in result:
            time.sleep(delay)
            continue

        for d in result.get("data", []):
            msg = d.get("message", "")
            if msg and caption.strip() in msg:
                return True
            
    return False