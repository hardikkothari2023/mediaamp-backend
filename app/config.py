import os

class Config:
     
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")

    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI",
        "postgresql://postgres:MediaAmp%40123@localhost/mediaamp"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
