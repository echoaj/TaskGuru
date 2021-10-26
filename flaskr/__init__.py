from flask import Flask
# We will be installing flask-sqlalchemy
# sqlalchemy is an ORM (Object Relational Mapper) which allows us to access DB in object oriented way.
# It's really good because you can use different databases without changing python code
from flask_sqlalchemy import SQLAlchemy
# Library for encrypting passwords
from flask_bcrypt import Bcrypt
# Library to control login sessions
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5e0a9b7327e6cec40d2d5c53f24d4bd'   # should make this an environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydata.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # set to function name of our route, tell where route is located
login_manager.login_message_category = 'info'   # make login message look nice using boostrap

from flaskr import routes