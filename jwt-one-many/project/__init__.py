from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

api = Api(app)

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-jwt-example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

from .users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')