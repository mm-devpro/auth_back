from os import getenv
from flask import Flask
from flask_restful import Api
from flask_login import LoginManager
from flask_cors import CORS
from dotenv import load_dotenv
from database import db

load_dotenv()
DB_USER = getenv('DB_USER')
DB_PWD = getenv('DB_PWD')
SECRET_KEY = getenv('SECRET_KEY')
MYSQL_URL = getenv('MYSQL_URL')
MYSQL_DB = getenv('MYSQL_DB')
MYSQL_PORT = getenv('MYSQL_PORT')


def create_app():
    # initiate app variable
    app = Flask(__name__)
    # app configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PWD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # initiate api from flask-restful, and add cors configuration
    # api = Api(app)
    CORS(app)

    # initiate app database
    with app.app_context():
        db.init_app(app)

    # configure authentication with Flask_Login then link it to flask
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        pass
        # since the user_id is just the primary key of our user table, use it in the query for the user
        # return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
