from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


DB_NAME = "database.db"
UPLOAD_FOLDER = "static/images"
SECRET_KEY = "odjfhkdf;a3423"
db = SQLAlchemy()
ma = Marshmallow()