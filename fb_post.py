import requests
from requests import JSONDecodeError
import time
from config import ACCESS_TOKEN, PAGE_ID

def post_to_facebook(image_url, caption):
    url = f'https://graph.facebook.com/v25.0/{PAGE_ID}/photos'

    payload = {
        'caption': caption,
        'access_token': ACCESS_TOKEN,
    }

    with open(image_url, 'rb') as f:
        files = {
            'source': f
        }

        response = requests.post(url, data=payload, files=files)

    # 1. Check HTTP layer
    if response.status_code not in [200, 201]:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    result = response.json()

    # 2. Success condition
    if "id" in result:
        return result

    # 3. Only fail if truly no success
    raise Exception(f"Unexpected response: {result}")

def check_post_if_error(caption, retries=5, delay=2):
    url = f'https://graph.facebook.com/v25.0/{PAGE_ID}/feed'

    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'message',
        'limit': 10  # recent posts only
    }

    for _ in range(retries):
        try:
            response = requests.get(url, params=params)
            result = response.json()

            if "error" in result:
                time.sleep(delay)
                continue

            for d in result.get("data", []):
                msg = d.get("message", "")
                if msg and caption.strip() in msg:
                    return True
        except JSONDecodeError: # HTTP 503 returns an HTML object
            pass
            
    return False
