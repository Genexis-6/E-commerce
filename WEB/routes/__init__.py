from .auth import auth
from .emailreg import email
from .home import home
from .service import service

def reg_route(app):
    app.register_blueprint(auth)
    app.register_blueprint(home)
    app.register_blueprint(email)
    app.register_blueprint(service)