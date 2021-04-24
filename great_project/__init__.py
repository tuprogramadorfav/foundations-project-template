from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os

# configure Flask using environment variables
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_user}:{db_password}@127.0.0.1/CEBJJ"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
manager = Manager(app)


from great_project import website