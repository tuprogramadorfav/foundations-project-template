from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, url_for, redirect, flash, request, jsonify, json
# from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from sqlalchemy import select
from flask_mail import Mail
from great_project.config import Config

import sys, os
import os

        

# configure Flask using environment variables


db = SQLAlchemy()
bcrypt = Bcrypt()
# connection = db.engine.connect()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Por favor inicie sesion para ver esta pagina!'
login_manager.login_message_category = 'info'
mail = Mail()

admin = Admin()
# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('users.login'))

# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('users.login'))

# class Llaves(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.is_admin

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('users.login'))
#     @expose('/')
#     def index(self):
#         all_belts = Belt.query.all()
#         all_ageDivision = Age_division.query.all()
#         return self.render('llaves.html')

# from great_project.models import Atleta, Academy, Event, Registration, Belt, Age_division
# admin.add_view(MyModelView(Atleta, db.session))
# admin.add_view(MyModelView(Academy, db.session))
# admin.add_view(MyModelView(Event, db.session))
# admin.add_view(MyModelView(Registration, db.session))
# admin.add_view(Llaves(name='Llaves', endpoint='llaves'))


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




