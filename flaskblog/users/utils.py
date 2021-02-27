import os, secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    im = im.convert('RGB')
    new_im = Image.new('RGB',(size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def save_picture(image):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(image.filename)
	file_name = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', file_name)

	output_size = (128,128)
	i = Image.open(image)
	squared_image = make_square(i)
	squared_image.thumbnail(output_size)
	squared_image.save(picture_path)

	return file_name

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message(
			f'Password Reset Confirmation for {user.username}',
			sender = 'noreply@demo.com',
			recipients = [user.email]
		)
	msg.body = f"""To reset your password, click the folowing link:
{url_for('users.reset_token',token=token, _external=True)}

Please ignore this message if you did not make this request.
"""
	mail.send(msg)