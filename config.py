from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
SECRET_KEY = os.environ.get("SECRET_KEY")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SMTP_USER = os.environ.get("SMTP_USER")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
REGION_NAME = os.environ.get("REGION_NAME")