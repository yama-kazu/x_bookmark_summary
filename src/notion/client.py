# src/notion/client.py

import os

import requests

from src.utils.logger import get_logger

logger = get_logger(__name__)


class NotionClient:
    def __init__(self, token: str = None):
        """
        Notion API クライアントの初期化

        Args:
            token (str): Notion Integration Token。省略時は .env の NOTION_API_KEY を使用
        """
        self.token = token or os.getenv("NOTION_API_KEY")
        if not self.token:
            raise ValueError("Notion API token is required")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def get_database(self, database_id: str):
        """データベース情報を取得"""
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            logger.error(f"Failed to get database: {response.text}")
            return None
        return response.json()

    def append_page(
        self, parent_database_id: str, properties: dict, children: list = None
    ):
        """
        データベースにページを追加

        Args:
            parent_database_id (str): 追加先データベースID
            properties (dict): ページのプロパティ
            children (list): ブロックの内容

        Returns:
            dict: 作成されたページの情報
        """
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": parent_database_id},
            "properties": properties,
        }
        if children:
            payload["children"] = children

        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            logger.error(f"Failed to create page: {response.text}")
            return None
        return response.json()
