import os
import secrets
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
current_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(current_dir,"models","database.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or secrets.token_hex(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    timezone = "Asia/Kolkata"
    enable_utc = False
    celerybeat_schedule_path = os.path.join(current_dir,"celerybeat","celerybeat-schedule")
    broker_url = "redis://127.0.0.1:6379/0"
    result_backend = "redis://127.0.0.1:6379/1"
    CACHE_REDIS_URL = "redis://127.0.0.1:6379/2"
    AUTH_REDIS_URL = "redis://127.0.0.1:6379/3"