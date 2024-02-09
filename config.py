import os
from dotenv import load_dotenv

load_dotenv()

class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    URL = os.environ["URL"]
    SECRET_KEY = "th15i5th3c0nf19p01nt-s3Cr3t-k3YS"
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
