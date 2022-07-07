import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'pavlo'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + 'app.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	AVATARS_SAVE_PATH = os.path.join(basedir, '/static/avatars')
	UPLOAD_FOLDER = os.path.join(basedir, 'app/static/avatars')