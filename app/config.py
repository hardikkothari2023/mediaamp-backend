import os

class Config:
    SECRET_KEY = "y1H@8xP!sD3#tK9v"  # Secure random key
    SQLALCHEMY_DATABASE_URI = "postgresql://mediaamp_user:MediaAmp%40123@127.0.0.1/mediaamp_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "X2pD!aL7#qRsM@5v"  # Secure JWT secret key
