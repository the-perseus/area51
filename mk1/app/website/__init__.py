from flask import Flask
from flask_sqlalchemy import SQLAlchemy #import modules
from os import path #for db check
from flask_login import LoginManager #for help with logins

db = SQLAlchemy()
DB_NAME = "database.db"
#sqlalchemy -> for the connection to db - db name!

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #Secure the cookies and session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #where the db is located -> in this case local in website folder! f=string function
    db.init_app(app)

    from .views import views #import the blueprint views
    from .auth import auth #import the blueprint auth

    app.register_blueprint(views, url_prefix='/') #register the blueprint: / because it is /views and not /something/views
    app.register_blueprint(auth, url_prefix='/') #register the blueprint: / because it is /views and not /something/views

    from .models import User, Note #import the models file and the user and note table/classes
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #redirect to auth.py with functions
    login_manager.init_app(app) #tell login manager which app

    @login_manager.user_loader #check for user id -> login process of login manager
    def load_user(id):
        return User.query.get(int(id)) #check primary key

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
#create the db if not exists already