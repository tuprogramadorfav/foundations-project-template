from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user




# configure Flask using environment variables
app = Flask(__name__)
engine = create_engine('postgresql://@127.0.0.1/CEBJJ')
connection = engine.connect()
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@127.0.0.1/CEBJJ'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
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

from great_project.models import Atleta, Academia, Event, Order
admin.add_view(MyModelView(Atleta, db.session))
admin.add_view(MyModelView(Academia, db.session))
admin.add_view(MyModelView(Event, db.session))
admin.add_view(MyModelView(Order, db.session))




from great_project import website