from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, fields, marshal_with
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
bcrypt = Bcrypt(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-jwt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Ill never tell'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

def authenticate(username, password):
    user = User.query.filter(User.username == username).first()
    if bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

@api.resource('/users')
class UserListAPI(Resource):
    @marshal_with(user_fields)
    def get(self):
        return User.query.all()

    @marshal_with(user_fields)
    def post(self):
        new_user = User(request.json['username'],request.json['password'])
        db.session.add(new_user)
        db.session.commit()
        return new_user

@api.resource('/users/<int:id>')
class UserAPI(Resource):
    @marshal_with(user_fields)
    @jwt_required()
    def get(self,id):
        return current_identity

    @marshal_with(user_fields)
    @jwt_required()
    def patch(self,id):
        current_identity.username = request.json['username']
        current_identity.password = bcrypt.generate_password_hash(request.json['password']).decode('UTF-8')
        db.session.add(current_identity)
        db.session.commit()
        return current_identity



jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    app.run(debug=True,port=3000)
