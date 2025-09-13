# src/line/notify.py

import os

import requests
from src.utils.logger import get_logger

logger = get_logger(__name__)

LINE_API_URL = "https://api.line.me/v2/bot/message/push"
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")


def send_line_message(to: str, message: str):
    """
    LINEにメッセージを送信
    :param to: ユーザーIDまたはグループID
    :param message: 送信メッセージ
    :return: True/False
    """
    if not ACCESS_TOKEN:
        logger.error("LINE_CHANNEL_ACCESS_TOKEN is not set in .env")
        return False

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {"to": to, "messages": [{"type": "text", "text": message}]}

    try:
        resp = requests.post(LINE_API_URL, headers=headers, json=payload)
        if resp.status_code != 200:
            logger.error(f"Failed to send LINE message: {resp.text}")
            return False
        logger.info(f"Sent LINE message to {to}")
        return True
    except Exception as e:
        logger.error(f"Exception sending LINE message: {e}")
        return False
