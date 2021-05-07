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
import sys, os
from os import environ

        

# configure Flask using environment variables
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
connection = db.engine.connect()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicie sesion para ver esta pagina!'
login_manager.login_message_category = 'info'

admin = Admin(app)
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class Llaves(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))
    @expose('/')
    def index(self):
        all_belts = Belt.query.all()
        all_ageDivision = Age_division.query.all()
        return self.render('llaves.html')

from great_project.models import Atleta, Academy, Event, Registration, Belt, Age_division
admin.add_view(MyModelView(Atleta, db.session))
admin.add_view(MyModelView(Academy, db.session))
admin.add_view(MyModelView(Event, db.session))
admin.add_view(MyModelView(Registration, db.session))
admin.add_view(Llaves(name='Llaves', endpoint='llaves'))




from great_project import website



