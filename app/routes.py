from app import app, db
from app.models import User, Post
from flask import request, render_template, redirect, url_for, flash
from app.forms import RegistrationForm, LoginForm, EditProfileForm, PostCreateForm
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
	posts = current_user.posts
	return render_template('index.html', title = 'Home', posts = posts)


@app.route('/explore')
@login_required
def explore():
	posts = Post.query.all()
	return render_template('explore.html', title = 'Explore	', posts = posts)


@app.route('/register', methods = ['POST', 'GET'])
def register():
	form = RegistrationForm()
	if request.method == 'POST':
		username = form.username.data
		email = form.email.data
		password = form.password.data
		password_confirm = form.password2.data
		user = User.query.filter_by(email = email).first()
		if user:
			flash('This is account already registered.')
			return redirect(url_for('register'))
		if password != password_confirm:
			flash('Confirm password not validate')
			return redirect(url_for('register'))
		user = User(username = username, email = email)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		login_user(user, remember=form.remember.data)
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form, title = 'Register')


@app.route('/login', methods = ['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.query.filter_by(username = username).first()
		if user == None:
			flash('Account')
			return redirect(url_for('login'))	
		if not user.check_password(password):
			flash('Invailid username/password')
			return redirect(url_for('login'))		
		login_user(user, remember=form.remember.data)
		return redirect(url_for('index'))
	else:
		return render_template('login.html', form = form, title = 'Login')

@app.route('/edit_profile', methods = ['POST', 'GET'])
def edit_profile():
	form = EditProfileForm(request.form, username = current_user.username, about_me = current_user.about_me)
	if request.method == 'POST':
		username = form.username.data
		about_me = form.about_me.data
		user = User.query.get(current_user.id)
		user.username = username
		user.about_me = about_me
		db.session.add(user)
		db.session.commit()
		file = request.files['image']
		if file:
			filename = str(current_user.id) + '.png'
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('Your changes have been saved.')
		return redirect(url_for('user', id = current_user.id))
	else:
		form.username.default = current_user.username
		form.about_me.default = current_user.about_me
		return render_template('edit_profile.html', form = form, title = 'Edit Profile')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash("You have been logged out.")
	return redirect(url_for('login'))


@app.route('/create_post', methods = ['POST', 'GET'])
def create_post():
	form = PostCreateForm()
	if request.method == 'POST':
		title = form.title.data
		intro = form.intro.data
		text = form.text.data
		post = Post(title = title, intro = intro, text = text, author = current_user)
		db.session.add(post)
		db.session.commit()
		flash('You create post!')
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form, title = 'Create Post')


@app.route('/user/<int:id>', methods = ['POST', 'GET'])
@login_required
def user(id):
	user = User.query.get(id)
	user_active = user.is_authenticated
	return render_template('user.html', title = 'Profile', user = user, user_active = user_active)


@app.route('/post/<int:id>', methods = ['POST', 'GET'])
@login_required
def post(id):
	post = Post.query.get(id)
	return render_template('post_details.html', title = post.title, post = post)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

