from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# configure Flask using environment variables
app = Flask(__name__)
engine = create_engine('postgresql://username:password@127.0.0.1/CEBJJ')
connection = engine.connect()
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@127.0.0.1/CEBJJ'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicie sesion para ver esta pagina'
login_manager.login_message_category = 'info'
from great_project import website