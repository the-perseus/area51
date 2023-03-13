from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "Hfb7395hBfg39gRg43"

# Configure SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.environ.get('MYSQL_USER', 'sqluser')}:{os.environ.get('MYSQL_PASSWORD', 'Vbg739gjbn83d')}@{os.environ.get('MYSQL_HOST', 'localhost')}/{os.environ.get('MYSQL_DB', 'userdb')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html", username=session["username"])
    else:
        return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        name = request.form["name"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        
        # Save data to database
        user = User(name=name, email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        # Store username in session
        session["username"] = username
        
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form["username"]
        password = request.form["password"]
        
        # Check if user exists in database
        user = User.query.filter_by(username=username, password=password).first()
        
        if user is not None:
            # Store username in session
            session["username"] = username
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    # Clear session data
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

