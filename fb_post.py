import requests
from config import ACCESS_TOKEN, PAGE_ID

def post_to_facebook(image_url, caption):
    url = f"https://graph.facebook.com/v25.0/{PAGE_ID}/photos"

    data = {
        "message": caption,
        "access_token": ACCESS_TOKEN
    }

    files = [
        ('source', ('image.jpg', open(image_url, 'rb'), 'image/jpeg'))
    ]

    response = requests.post(url, data=data, files=files)
    result = response.json()

    if "error" in result:
        raise Exception(result["error"])

    return result