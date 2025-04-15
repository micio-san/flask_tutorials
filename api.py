from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

# Create an instance of the Flask class
app = Flask(__name__)

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

# Initialize the database connection
db = SQLAlchemy(app)
api = Api(app)

# Define the UserModel
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User ({self.name}), email=({self.email}), id=({self.id})"

# Request parser for user arguments
user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str, required=True, help="The name cannot be blank")
user_args.add_argument("mail", type=str, required=True, help="The email cannot be blank")

# Fields for marshalling responses
userFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String
}

# Resource for handling multiple users
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["mail"])
        db.session.add(user)
        db.session.commit()
        return user, 201

# Resource for handling a single user
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        return user

    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        user.name = args["name"]
        user.email = args["mail"]
        db.session.commit()
        return user, 200

    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return "", 204

# Add resources to the API
api.add_resource(User, "/api/users/<int:id>")
api.add_resource(Users, "/api/users/")

# Define the home route
@app.route('/')
def home():
    return "I am the homepage"

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
