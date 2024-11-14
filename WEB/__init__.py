from flask import Flask
from .routes import reg_route
from .ext import db, migrate, login_manager, mail
from .model import Customers, Category



def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    
    
    reg_route(app)
    
    
    # login users
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    @login_manager.user_loader
    def load_user(user_id):
        return Customers.query.get(int(user_id))
    
    return app