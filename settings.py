import os

from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
STUDENT_TOKEN = os.environ.get("STUDENT_TOKEN")
TEACHER_TOKEN = os.environ.get("TEACHER_TOKEN")
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN")
