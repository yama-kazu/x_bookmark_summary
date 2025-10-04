# src/openai/summarize.py

import os

from dotenv import load_dotenv

from openai import OpenAI
from src.utils.logger import get_logger

logger = get_logger(__name__)

# .env ファイルの読み込み
load_dotenv()

# OpenAIクライアントの初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_tweets(tweets, model="gpt-4o", max_results=7):
    """
    Xのブックマークを要約する関数。
    必要に応じてWeb検索を行い、最新情報を取得します。

    Args:
        tweets (list[dict]): Xのブックマークデータのリスト
        model (str): 使用するOpenAIモデル
        max_results (int): 要約するツイートの最大件数
    Returns:
        summaries (list[dict]): 要約結果のリスト
    """
    summaries = []
    for tweet in tweets[:max_results]:
        text = tweet.get("text", "")
        if not text:
            continue

        try:
            # OpenAI Responses APIを使用して要約を生成
            response = client.responses.create(
                model=model,
                input="あなたは優秀なデータサイエンティストです。以下の投稿内容および添付されているWebページの内容を必ず2000字以内に要約し、有益な情報を提供してください。\n"
                + text,
                tools=[{"type": "web_search"}],  # Web検索を含むツールを指定
                max_output_tokens=10000,
            )
            summary = response.output_text.strip()
            summaries.append(
                {
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "summary": summary,
                }
            )
        except Exception as e:
            logger.error(f"Error summarizing tweet {tweet['id']}: {e}")
            summaries.append(
                {
                    "id": tweet["id"],
                    "text": tweet["text"],
                    "summary": None,
                }
            )

    return summaries
