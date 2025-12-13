# modules/api_utils.py
import requests

def get_cat_camera_image(api_url, params=None):
    """Fetch image from a cat camera API"""
    try:
        response = requests.get(api_url, params=params)
        if response.status_code == 200:
            return response.content  # return image bytes
        else:
            print("API request failed:", response.status_code)
            return None
    except Exception as e:
        print("Error fetching API:", e)
        return None
