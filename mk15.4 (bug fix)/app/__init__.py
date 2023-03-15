from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

def create_all():
    with app.app_context():
        from app.models import Base
        alembic_tables = [t.name for t in db.engine.table_names() if t.startswith('alembic_')]
        Base.metadata.create_all(bind=db.engine, tables=[t for t in Base.metadata.sorted_tables if t.name not in alembic_tables])

from app import routes, models