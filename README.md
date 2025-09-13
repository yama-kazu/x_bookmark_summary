# X Bookmark Summarizer

## 概要
このアプリケーションは、X（旧Twitter）でブックマークした投稿を取得し、OpenAI APIを利用して要約します。
要約結果はNotionに保存され、LINEで通知されます。
日次自動実行や、Windows上でのローカル運用も可能です。

## フォルダ構成
```
app
├ src/
│   ├ x_bookmark/        # X API ブックマーク取得関連
│   │   ├ auth.py        # OAuth2.0認証・refresh_token管理
│   │   └  fetch.py       # ブックマーク取得処理
│   │
│   ├ openai/            # OpenAI 要約関連
│   │   └ summarize.py   # OpenAI Responses APIを使った要約処理
│   │
│   ├ notion/            # Notion API 連携
│   │   ├ client.py      # Notion APIクライアント
│   │   └ writer.py      # Notionに要約結果を書き込む処理
│   │
│   ├ line/              # LINE通知関連
│   │   └ notify.py      # LINE Messaging APIを使った通知
│   │
│   └ utils/             # 共通ユーティリティ
│       ├ config.py      # .env読み込み・共通設定
│       └ logger.py      # ロギング共通処理
│
├ tests/                 # 単体テスト
│   ├ test_x_bookmark.py # X APIブックマーク取得のテスト
│   ├ test_openai.py     # OpenAI要約処理のテスト
│   ├ test_notion.py     # Notion出力処理のテスト
│   └ test_line.py       # LINE通知処理のテスト
│
├ .env                   # APIキーやシークレットを管理（CLIENT_ID, REFRESH_TOKENなど）
├ pyproject.toml         # uv/Poetry用パッケージ管理ファイル
├ README.md              # プロジェクト概要・セットアップ方法
└ main.py                # アプリケーション起動スクリプト
```


## 環境変数 (.env)
- CLIENT_ID, CLIENT_SECRET: X API クライアント情報
- REFRESH_TOKEN: X API OAuth2.0 User Context トークン
- OPENAI_API_KEY: OpenAI APIキー
- NOTION_API_KEY: Notion Integration Token
- LINE_CHANNEL_ACCESS_TOKEN: LINE Messaging API用トークン
- LINE_USER_ID: LINE通知先のユーザーIDまたはグループID

## セットアップ
1. リポジトリをクローン
2. `.env` を作成して環境変数を設定
3. 必要なライブラリをインストール
```bash
uv sync
```
4. `main.py`を実行
```bash
uv run main.py
```



