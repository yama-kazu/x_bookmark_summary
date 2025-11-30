# X Bookmark Summarizer

## 概要
このアプリケーションは、X（旧Twitter）でブックマークした投稿を取得し、OpenAI APIを利用して要約した結果をNotionに保存します。

## フォルダ構成
```
x_bookmark_summary
├ src/
│   ├ x_bookmark/        # X API ブックマーク取得関連
│   │   ├ auth.py        # OAuth2.0認証・refresh_token管理
│   │   └ fetch.py       # ブックマーク取得処理
│   │
│   ├ openai/            # OpenAI 要約関連
│   │   └ summarize.py   # OpenAI Responses APIを使った要約処理
│   │
│   ├ notion/            # Notion API 連携
│   │   ├ client.py      # Notion APIクライアント
│   │   └ writer.py      # Notionに要約結果を書き込む処理
│   │
│   └ utils/             # 共通ユーティリティ
│       ├ config.py      # .env読み込み・共通設定
│       └ logger.py      # ロギング共通処理
│
├ .env                   # APIキーやシークレットを管理（CLIENT_ID, REFRESH_TOKENなど）※各自で用意
├ pyproject.toml         # uv/Poetry用パッケージ管理ファイル
├ uv.lock                # uv/Poetry用パッケージ管理ファイル
├ README.md              # プロジェクト概要・セットアップ方法
└ main.py                # アプリケーション起動スクリプト
```


## 環境変数 (.env)
下記の情報を記載した.envファイルを作成してください
- CLIENT_ID: X API クライアント情報
- CLIENT_SECRET: X API クライアント情報
- OPENAI_API_KEY: OpenAI APIキー
- NOTION_DATABASE_ID: Notion データベースID
- NOTION_API_KEY: Notion Integration Token

※X APIに関する情報の取得方法は次のZennにまとめたのでそちらを参照：[X APIの利用方法](https://zenn.dev/kazu_yama/articles/f415d957f4a791)  
※REFRESH_TOKEN: X API OAuth2.0 User Context トークン  は自動で書き込まれるため記載不要！


## セットアップ
1. リポジトリをクローン
2. `.env` を作成して変数を設定

## 実行
### ローカル環境で実行する場合
1. 必要なライブラリをインストール
```bash
uv sync
```
2. `main.py`を実行
```bash
uv run main.py
```

### Cloud Run (Google Cloud)で実行する場合
※ Google Cloudのログインは完了しているものとします  
※ {{}}で囲んでいる変数は適宜当てはめて実行してください
1. .env を Secret Managerに登録（今回はまとめて登録してしまいます）
```bash
gcloud secrets create app-env --data-file=.env
```

※ 環境変数を更新する場合
```bash
gcloud secrets versions add app-env --data-file=.env
```

2. Docker imageのbuild & push
```bash
gcloud builds submit --tag "asia-northeast1-docker.pkg.dev/{{ project_id }}/{{ artifact_repo }}/{{ image_name }}"
```

3. Cloud Run Jobs の作成（初回）
```
gcloud run jobs create {{ job_name }} \
  --image="asia-northeast1-docker.pkg.dev/{{ project_id }}/{{ artifact_repo }}/{{ image_name }}" \
  --region=asia-northeast1 \
  --set-secrets=".env=projects/{{ project_number }}/secrets/app-env:latest"
```

※ 上書きする場合
```bash
gcloud run jobs update {{ job_name }} \
  --image="asia-northeast1-docker.pkg.dev/{{ project_id }}/{{ artifact_repo }}/{{ image_name }}" \
  --region=asia-northeast1 \
  --set-secrets=".env=projects/{{ project_number }}/secrets/app-env:latest"
```

4. Cloud Run Jobの手動実行
```bash
gcloud run jobs execute {{ job_name }} --region=asia-northeast1
```

5. （参考）定期実行の設定
まず Cloud Run Job の execution URI を取得。
```bash
gcloud run jobs describe {{ job_name }} --region asia-northeast1 \
  --format="value(status.executionUri)"
```
その URI を使って Scheduler を作成:
```bash
gcloud scheduler jobs create http {{ scheduler_job_name }} \
  --schedule="{{ cron }}" \
  --uri="{{ job_execution_uri }}" \
  --http-method=POST \
  --location=asia-northeast1
```



