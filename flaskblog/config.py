import os

class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('SC_DB_URI')
	# SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	SECRET_KEY = os.environ.get('SC_SECRET_KEY')
	# SECRET_KEY = '93fcca7d58d595b07316b21e744b38af'
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('SC_EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('SC_EMAIL_PASS')