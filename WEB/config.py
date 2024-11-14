from dotenv import load_dotenv
from datetime import timedelta
import os


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = os.getenv("DEBUG")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR,"static", 'images', 'photos')
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    
    
    
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFCATION = False
        



class ProductionConfig(Config):
    DEBUG = os.getenv("DEBUG")
    