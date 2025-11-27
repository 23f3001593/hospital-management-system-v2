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
    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_ENABLE_UTC = False
    CELERYBEAT_SCHEDULE_PATH = os.path.join(current_dir,"celerybeat","celerybeat-schedule")
    REDIS_AUTH_URL = "redis://127.0.0.1:6379/0"
    REDIS_CACHE_URL = "redis://127.0.0.1:6379/1"
    CELERY_BROKER_URL = "redis://127.0.0.1:6379/2"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/3"
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025
    MAIL_USERNAME = os.getenv("MAIL_USERNAME") or None
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD") or None
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False