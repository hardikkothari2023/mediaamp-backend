import os

class Config:
    # Load secret keys securely
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")

    # PostgreSQL DB
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "postgresql://postgres:MediaAmp%40123@localhost/mediaamp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis broker (used by Celery and for caching)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
