import requests

from src.utils.logger import get_logger
from src.x_bookmark.auth import get_access_token

logger = get_logger(__name__)

BASE_URL = "https://api.twitter.com/2"


def fetch_bookmarks(max_results: int = 10):
    """
    X API を使って自分のブックマークを取得

    Args:
        max_results (int): 取得件数（最大100）
    Returns:
        bookmarks_list (list): ブックマークのリスト（JSON）
    """
    access_token = get_access_token()
    if not access_token:
        logger.error("Failed to get access token.")
        return []

    # 自分のユーザーIDを取得
    me_url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = requests.get(me_url, headers=headers)
    if me_response.status_code != 200:
        logger.error(f"Failed to get user info: {me_response.text}")
        return []
    user_id = me_response.json()["data"]["id"]

    # ブックマーク取得
    bookmarks_url = f"{BASE_URL}/users/{user_id}/bookmarks"
    params = {"max_results": max_results, "tweet.fields": "created_at"}
    response = requests.get(bookmarks_url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"Failed to fetch bookmarks: {response.text}")
        return []

    data = response.json()
    bookmarks_list = data.get("data", [])
    logger.info(f"Fetched {bookmarks_list} bookmarks.")
    return bookmarks_list
