from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

app = Flask(__name__)
CSRFProtect(app)

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models