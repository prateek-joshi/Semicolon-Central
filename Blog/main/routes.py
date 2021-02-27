from flask import Blueprint, render_template, request
from flaskblog.models import Post

main = Blueprint('main', '__name__')

@main.route('/homepage')
@main.route('/')
def homepage():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=6)
	return render_template('home.html',posts=posts)

@main.route('/about-us')
def about_us():
	return render_template('about-us.html', title='About')

