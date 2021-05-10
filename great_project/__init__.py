from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from great_project.config import Config
import sys, os

    
# configure Flask using environment variables
db = SQLAlchemy()
bcrypt = Bcrypt()
# connection = db.engine.connect()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Por favor inicie sesion para ver esta pagina!'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    # connection.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from great_project.users.routes import users
    from great_project.event.routes import event
    from great_project.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(event)
    app.register_blueprint(main)
    return app





