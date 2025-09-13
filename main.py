# from src.line import notify as line_notify
# from src.notion import writer as notion_writer
from src.openai import summarize
from src.utils.logger import get_logger
from src.x_bookmark import fetch as x_fetch

logger = get_logger(__name__)


def main():
    logger.info("Starting X Bookmark Summarizer")

    # 1. Xブックマーク取得
    max_results = 3  # 取得件数はここで調整可能
    try:
        bookmarks = x_fetch.fetch_bookmarks(max_results=max_results)
        logger.info(f"Fetched {len(bookmarks)} bookmarks")
    except Exception as e:
        logger.error(f"Error fetching bookmarks: {e}")
        return

    if not bookmarks:
        logger.info("No bookmarks to process")
        return

    # 2. OpenAIで要約
    try:
        summaries = summarize.summarize_tweets(bookmarks)
        logger.info(f"Generated {len(summaries)} summaries")
    except Exception as e:
        logger.error(f"Error summarizing tweets: {e}")
        return

    for summary in summaries:
        print(
            f"Tweet ID: {summary['id']}\nTweet: {summary['text']}\nSummary: {summary['summary']}\n"
        )
    # 3. Notionに書き込み
    # notion_db_id = get_env("NOTION_DATABASE_ID")
    # if not notion_db_id:
    #     logger.error("NOTION_DATABASE_ID is not set in .env")
    #     return

    # try:
    #     notion_writer.write_to_notion(summaries, database_id=notion_db_id)
    #     logger.info("Summaries written to Notion")
    # except Exception as e:
    #     logger.error(f"Error writing to Notion: {e}")
    #     return

    # 4. LINEに通知
    # line_to = get_env("LINE_USER_ID")
    # if line_to:
    #     message = f"New {len(summaries)} tweet summaries added to Notion."
    #     success = line_notify.send_line_message(to=line_to, message=message)
    #     if success:
    #         logger.info("LINE notification sent")
    #     else:
    #         logger.error("Failed to send LINE notification")


if __name__ == "__main__":
    main()
