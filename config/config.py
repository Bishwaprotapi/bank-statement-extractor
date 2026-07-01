import os

class Config:
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    CORS_HEADERS = "Content-Type"

