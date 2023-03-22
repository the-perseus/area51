from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    logbookentry = db.relationship('Logbooktable', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
        }
        if include_email:
            data['email'] = self.email
        return data       
              
              
    @staticmethod
    def current_user():
        return current_user._get_current_object()
        
    def to_collection():
        users = User.query.all()
        data = {'items': [item.to_dict() for item in users]}
        return(data)    
        
        

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Logbooktable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    time = db.Column(db.Integer)
    depth = db.Column(db.Float)
    temperature = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #user = db.relationship('User', backref='Logbooktable')
    
    def to_dict(self):
        data = {
            'location': self.location,
            'time': self.time,
            'depth': self.depth,
            'temperature': self.temperature,
            'user_id': self.user_id,
            
        }
        
    @staticmethod    
    def to_collection():
        logbook = Logbooktable.query.all()
        data = {'items': [item.to_dict() for item in logbook]}
        return(data)     