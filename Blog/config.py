import os

class Config:
	SQLALCHEMY_DATABASE_URI = os.environ.get('SC_DB_URI')
	SECRET_KEY = os.environ.get('SC_SECRET_KEY')
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('SC_EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('SC_EMAIL_PASS')