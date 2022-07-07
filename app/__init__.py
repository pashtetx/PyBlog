from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from config import Config
from flask_login import LoginManager

app = Flask(__name__)
bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config.from_object(Config)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


with app.app_context():
    from app.models import User, Post 
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).get(user_id)

from app import routes, models
