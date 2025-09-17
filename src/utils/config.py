# src/utils/config.py

import os

from dotenv import load_dotenv

# .env をロード
load_dotenv()


def get_env(key: str, default=None):
    """
    環境変数を取得するヘルパー関数

    Args:
        key (str): 環境変数名
        default: 値がなかった場合のデフォルト

    Returns:
        環境変数の値
    """
    return os.getenv(key, default)
