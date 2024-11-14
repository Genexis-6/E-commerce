from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import URLSafeSerializer
from flask_login import LoginManager, current_user, login_user, logout_user, UserMixin, login_required
from .config import Config
from flask_mail import Mail, Message
from random import randint

migrate = Migrate()
db = SQLAlchemy()
config = Config()
login_manager = LoginManager()
mail = Mail()

# csrf token generator
serializer = URLSafeSerializer(config.SECRET_KEY)


def generate_csrf_token():
    return serializer.dumps("csrf_token", salt="csrf-protection")


def validate_csrf_token(token):
    try:
        serializer.loads(token, salt="csrf-protection", max_age=3600)
        return True
    except:
        return False
    
    
# upload file
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowd_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# otp generator

def otp():
    num = ''
    for _ in range(6):
        num += str(randint(0, 9))
    return num
