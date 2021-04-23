from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# configure Flask using environment variables
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.config['SECRET_KEY'] = '802023d0df4b9ee3a0341a80847a7e0b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:programanding@programanding-VirtualBox/CEBJJ'
db = SQLAlchemy(app)


from great_project import website