from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_URI = 'sqlite:///flask-test.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.secret_key = 'secret'

db = SQLAlchemy(app)

