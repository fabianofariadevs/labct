from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'SOXOZvMJBD')
app.config.from_object('config.Config')

db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager(app)


