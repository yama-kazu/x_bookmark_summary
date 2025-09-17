from src.notion.client import NotionClient
from src.utils.logger import get_logger

logger = get_logger(__name__)


def write_to_notion(summaries: list, database_id: str):
    """
    要約結果をNotionに書き込む

    Args:
        summaries (list[dict]): [{'id': tweet_id, 'text': text, 'summary': text}, ...]
        database_id (str): NotionデータベースID
    Returns:
        results (list): 書き込み結果のリスト
    """
    client = NotionClient()
    results = []

    for item in summaries:
        tweet_id = item.get("id")
        tweet_text = item.get("text", "")
        summary = item.get("summary", "")

        output_text = f"# 元の投稿:\n{tweet_text}\n\n# 要約:\n{summary}"

        if not summary:
            logger.warning(f"Skipping tweet {tweet_id}: summary is empty")
            continue

        # ページのプロパティ
        properties = {"Name": {"title": [{"text": {"content": f"Tweet {tweet_id}"}}]}}

        # 本文をブロックとして追加
        children = [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": output_text},
                        }
                    ]
                },
            },
        ]

        page = client.append_page(database_id, properties, children)
        results.append(page)
        logger.info(f"Written tweet {tweet_id} to Notion")

    return results
