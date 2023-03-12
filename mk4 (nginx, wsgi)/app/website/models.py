from . import db #import db
from flask_login import UserMixin #module to login users for sql -> tool for help
from sqlalchemy.sql import func #for the time function below -> automatic function for db


class Note(db.Model): #inherit from db-model (schema)
    id = db.Column(db.Integer, primary_key=True) #id as primary_key
    data = db.Column(db.String(10000)) #string max 10k in this case, possible more
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #timestamp inlc timezone
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #connection to the userclass+id below -> every entry have a user. One to many relationship. One User=Many Entrys.


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) #id as primary_key
    email = db.Column(db.String(150), unique=True) #string max 150 in this case. Unique=no double mail adresses
    password = db.Column(db.String(150)) #string max 150 in this case
    first_name = db.Column(db.String(150)) #string max 150 in this case
    notes = db.relationship('Note') #relation to the note table
#defining the user table with the UserMixin module (just for user table!)