import os
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv, set_key
from flask import Flask, redirect, request

from src.utils.logger import get_logger

logger = get_logger(__name__)

# .env ファイルの読み込み
load_dotenv()

CLIENT_ID = os.getenv("X_CLIENT_ID")
CLIENT_SECRET = os.getenv("X_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8080/callback"
TOKEN_URL = "https://api.twitter.com/2/oauth2/token"
AUTH_URL = "https://twitter.com/i/oauth2/authorize"
SCOPE = ["tweet.read", "users.read", "bookmark.read", "offline.access"]

ENV_PATH = ".env"


def get_stored_refresh_token():
    return os.getenv("X_REFRESH_TOKEN")


def store_refresh_token(token: str):
    """更新された refresh_token を .env に保存"""
    set_key(ENV_PATH, "X_REFRESH_TOKEN", token)


def refresh_access_token(refresh_token: str):
    """refresh_token を使ってアクセストークンを更新"""
    logger.info("Refreshing access token...")
    data = {
        "client_id": CLIENT_ID,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = requests.post(
        TOKEN_URL,
        data=data,
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code != 200:
        logger.error(f"Failed to refresh token: {response.text}")
        return None, None
    tokens = response.json()
    if "refresh_token" in tokens:
        store_refresh_token(tokens["refresh_token"])
    return tokens.get("access_token")


def start_flask_auth():
    app = Flask(__name__)

    @app.route("/")
    def login():
        query = {
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "scope": " ".join(SCOPE),
            "state": "state123",
            "code_challenge": "challenge",
            "code_challenge_method": "plain",
        }
        return redirect(f"{AUTH_URL}?{urlencode(query)}")

    @app.route("/callback")
    def callback():
        code = request.args.get("code")
        if not code:
            return "No code provided", 400

        data = {
            "client_id": CLIENT_ID,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
            "code_verifier": "challenge",
        }
        response = requests.post(
            TOKEN_URL,
            data=data,
            auth=(CLIENT_ID, CLIENT_SECRET),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if response.status_code != 200:
            return f"Error: {response.text}", 400

        tokens = response.json()
        if "refresh_token" in tokens:
            store_refresh_token(tokens["refresh_token"])
        logger.info("Authentication successful. Tokens stored.")
        return "Authentication successful. You can close this window."

    app.run(port=8080, debug=True)


def get_access_token():
    refresh_token = get_stored_refresh_token()
    if refresh_token:
        access_token = refresh_access_token(refresh_token)
        if access_token:
            return access_token
        logger.warning("Stored refresh token invalid, starting new auth flow...")
    start_flask_auth()
    return None
