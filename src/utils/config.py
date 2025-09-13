# src/utils/config.py

import os

from dotenv import load_dotenv

# .env をロード
load_dotenv()


def get_env(key: str, default=None):
    """
    環境変数を取得するヘルパー関数
    :param key: 環境変数名
    :param default: 値がなかった場合のデフォルト
    :return: 環境変数の値
    """
    return os.getenv(key, default)
