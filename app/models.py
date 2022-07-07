from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
	id = db.Column(db.Integer(), primary_key=True)
	username = db.Column(db.String(50), nullable=False, unique=True)
	email = db.Column(db.String(100), nullable=False, unique=True)
	last_seen = db.Column(db.DateTime, default = datetime.utcnow)
	password_hash = db.Column(db.String(100), nullable=False)
	about_me = db.Column(db.String(200))

	avatar = db.Column(db.Integer, default = 0)
	posts = db.relationship('Post', backref='author', lazy='dynamic')




	def __repr__(self):
		return "<{}:{}>".format(self.id, self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,  password):
		return check_password_hash(self.password_hash, password)

	def check_is_active(self, )


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	intro = db.Column(db.String(100))
	text = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))