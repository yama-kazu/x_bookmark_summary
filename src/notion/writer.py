# src/notion/writer.py

from src.utils.logger import get_logger

from src.notion.client import NotionClient

logger = get_logger(__name__)


def write_to_notion(summaries, database_id):
    """
    要約結果をNotionに書き込む
    :param summaries: [{'id': tweet_id, 'summary': text}, ...]
    :param database_id: NotionデータベースID
    :return: 書き込み結果のリスト
    """
    client = NotionClient()
    results = []

    for item in summaries:
        tweet_id = item.get("id")
        summary = item.get("summary", "")

        if not summary:
            logger.warning(f"Skipping tweet {tweet_id}: summary is empty")
            continue

        # ページのプロパティ
        properties = {
            "Name": {"title": [{"text": {"content": f"Tweet {tweet_id}"}}]},
        }

        # 本文をブロックとして追加
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"text": [{"type": "text", "text": {"content": summary}}]},
            }
        ]

        page = client.append_page(database_id, properties, children)
        results.append(page)
        logger.info(f"Written tweet {tweet_id} to Notion")

    return results
