import requests
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