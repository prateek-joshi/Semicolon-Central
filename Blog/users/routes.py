from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
							 RequestResetForm, ResetPasswordForm)
from flaskblog.posts.forms import PostForm
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', '__name__')

@users.route('/register',methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.homepage'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You can log in.', 'sucess')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)

@users.route('/login',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.homepage'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				flash(f'Logged in successfully as {user.username}!','success')
				return redirect(next_page)
			else:
				flash(f'Logged in successfully as {user.username}!','success')
				return redirect(url_for('main.homepage'))
		else:
			flash(f'Login unsuccessful. Please check email and password.','danger')
	return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('users.login'))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
	image_file = url_for('static', filename='profile_pics/'+current_user.profile)
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.profile = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!','success')
		return redirect(url_for('users.account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	#return render_template('account.html', title='Account')
	return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route('/user/<string:username>')
def user_posts(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	image_file = url_for('static', filename='profile_pics/'+user.profile)
	posts = Post.query\
			.filter_by(author=user)\
			.order_by(Post.date.desc())\
			.paginate(page=page, per_page=6)
	return render_template('user_posts.html',posts=posts, user=user, image_file=image_file)
	# return render_template('user_posts.html',posts=posts, user=user)

@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.homepage'))
	form = RequestResetForm()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password.', 'success')
		return redirect(url_for('users.login'))

	return render_template('reset_request.html',title='Reset Password',form=form)

@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.homepage'))
	user = User.verify_reset_token(token)
	if user is None:
		flash(f'Invalid/Expired Token.', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_pwd
		db.session.commit()
		flash(f'Your password has been changed!', 'sucess')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)