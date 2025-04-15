from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
#This line creates an instance of the Flask class. 
#The __name__ variable is passed to the Flask constructor, 
#which helps Flask determine the root path of the application.
app = Flask(__name__);

#The line of code you provided is used to configure the database URI for a Flask application that uses 
# SQLAlchemy as its ORM (Object-Relational Mapping) tool. This configuration specifies that the application should use an SQLite database stored in a file named test.db.
#app.config: This is a dictionary-like object in Flask where you can store configuration variables for your application.
#SQLALCHEMY_DATABASE_URI: This is a configuration key used by SQLAlchemy to specify the database connection URI. The URI format depends on the type of database you are using.
#sqlite:///test.db: This URI specifies that SQLite should be used as the database, and the database file is named test.db. 
# The three slashes (///) indicate an absolute path to the database file. If you use four slashes (////), it indicates a relative path.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
# Initialize the database connection
db= SQLAlchemy(app)
#decorator
@app.route('/')

class UserModel(db.Model):
     id=db.Column(db.Integer, primary_key=True);
     #nullable= NULL
     name=db.Column(db.String(80),unique=True, nullable=False);
     email=db.Column(db.String(80), unique=True, nullable=False);
     def _repr__(self):
         return f"User ({self.name}), email=({self.mail}), id=({self.id})"

def home():
    return "I am the homepage"

if __name__ == "__main__":
    #This line checks if the script is being run directly (not imported as a module).
    #If it is, it calls the run method on the app instance to start the Flask development server.
    app.run(debug=True)
