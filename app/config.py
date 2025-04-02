import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://mediaamp_user:MediaAmp@123@localhost/mediaamp_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
