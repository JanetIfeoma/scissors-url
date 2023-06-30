from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db =SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] ='4dbd2e68bf5f7t7juu3e3341180c13d'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    app.register_blueprint(auth, url_prefix="/")
    # app.register_blueprint(short)


    from .models import User, Link
    create_database(app)


    lmanager =  LoginManager()
    lmanager.login_view = "auth.login"
    lmanager.init_app(app)

    @lmanager.user_loader
    def load_user(id):
     return User.query.get(int(id))

    
    
    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
       app.app_context().push()
       db.create_all()
    print("Database Created!!")