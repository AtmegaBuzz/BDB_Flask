import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
DB_NAME = "database.db"
ma = Marshmallow()

def create_app():

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "adsdklajer234"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from backend.auth import auth 
    from backend.views import views

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/auth/')


    from backend.models import (
        User,
        Person,
        Image,
        Location,
        UserTypeEnum
    )

    create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # serialize/deserialize library 
    ma.init_app(app)    

    return app


def create_database(app):

    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print("database created...")