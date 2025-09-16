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
        processed_bookmarks (list): ブックマークツイートのリスト（JSON）
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
    params = {
        "max_results": max_results,
        "tweet.fields": "id,text,entities",  # 取得する項目【参考：https://docs.x.com/x-api/fundamentals/data-dictionary】
    }
    response = requests.get(bookmarks_url, headers=headers, params=params)
    if response.status_code != 200:
        logger.error(f"Failed to fetch bookmarks: {response.text}")
        return []

    data = response.json()
    bookmarks = data.get("data", [])

    # ツイート内のURL展開処理
    processed_bookmarks = []
    for tweet in bookmarks:
        text = tweet.get("text", "")
        entities = tweet.get("entities", {})
        urls = entities.get("urls", [])

        for url_obj in urls:
            short_url = url_obj.get("url")
            expanded_url = url_obj.get("expanded_url")
            if short_url and expanded_url:
                text = text.replace(short_url, expanded_url)

        tweet["text"] = text
        processed_bookmarks.append(tweet)

    logger.info(f"Fetched {processed_bookmarks} bookmarks.")
    return processed_bookmarks
