from flask import Blueprint, render_template, request, flash, redirect, url_for #import. request for methods.
from .models import User #import user
from werkzeug.security import generate_password_hash, check_password_hash #import for hashing the password from users to the db, important for security! Because with a hash only to check IF the pw is legit (as user types in), but not can read it
from . import db   #means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user #import. redirect for user redirect. flask login/logout/etc module to restrict access to home

#basically 3 routes for AUTH Process: /login, /logout and /signup PAGES, test it first with simple text


auth = Blueprint('auth', __name__) #naming blueprint, this case auth


@auth.route('/login', methods=['GET', 'POST']) #call route login and add functions GET (read) and POST (create method), GET because read first and then create (button)
def login():
    if request.method == 'POST': #if login and not just read (GET)
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first() #check the db table (basic filter function), first because it should only be 1 entry
        if user:
            if check_password_hash(user.password, password): #ask the db about the pw input (hash compare against input hash)
                flash('Logged in successfully!', category='success') #feedback to user if correct
                login_user(user, remember=True) #remember function (saves in flask session, as long webserver runs)
                return redirect(url_for('views.home')) #send user to home
            else:
                flash('Incorrect password, try again.', category='error') #feedback if wrong
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user) #call the login.html template/design, user -> pass it from login.html. Also possible to make an if true boolean from login.html.


@auth.route('/logout')
@login_required #make sure can not access without logged in status
def logout():
    logout_user() #forget the user
    return redirect(url_for('auth.login')) #send to login page


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #what happens after button pressed -> POST request

        user = User.query.filter_by(email=email).first()
        if user: #cehck if user email already exists
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256')) #user creation in db -> input writing to the db. Take password1 (input) and hash it with SHA256
            db.session.add(new_user) #add
            db.session.commit() #commit
            login_user(new_user, remember=True) #to be loged in after register
            flash('Account created!', category='success') #flash function using flask -> fancy info message, optional design stuff
            return redirect(url_for('views.home')) #send user to the homepage home after user have signed up
            
           # the function basically control the inputs to check wrong inputs with simple if-function, also pw hashing intergrated and write to db

    return render_template("sign_up.html", user=current_user) #call the signup template, user current state function for the navbar function home button

