from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# configure Flask using environment variables
app = Flask(__name__)
engine = create_engine('postgresql://programanding:Isaaceinstein21@127.0.0.1/CEBJJ')
connection = engine.connect()
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://programanding:Isaaceinstein21@127.0.0.1/CEBJJ'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from great_project import website