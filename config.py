import pymysql
import sentry_sdk
import os
from dotenv import load_dotenv

# =========================
# CONFIG
# =========================
load_dotenv()

DB_CONFIG = {
    "host": os.getenv('HOST'),
    "user": os.getenv('USER'),
    "password": os.getenv('PASSWORD'),
    "database": os.getenv('DATABASE'),
    "cursorclass": pymysql.cursors.DictCursor
}

ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('PAGE_ID')

POST_INTERVAL = 600  # seconds

# Sentry
sentry_sdk.init(
    dsn="your_sentry_dsn",
    traces_sample_rate=0.0
)
