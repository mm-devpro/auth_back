from os import environ, path
import sys
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from database import db, ma
from service.auth import decode_cookie

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

load_dotenv()
DB_USER = environ['DB_USER']
DB_PWD = environ['DB_PWD']
SECRET_KEY = environ['SECRET_KEY']
MYSQL_URL = environ['MYSQL_URL']
MYSQL_DB = environ['MYSQL_DB']
MYSQL_PORT = environ['MYSQL_PORT']
JWT_SECRET_KEY = environ['JWT_SECRET_KEY']


def create_app():
    # initiate app variable
    app = Flask(__name__)
    # app configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PWD}@{MYSQL_URL}:{MYSQL_PORT}/{MYSQL_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # initiate api from flask-restful, and add cors configuration
    # api = Api(app)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    # initiate app database
    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

    # blueprint for auth routes in our app
    from route import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from route import home as home_blueprint
    app.register_blueprint(home_blueprint)
    from route import cam as cam_blueprint
    app.register_blueprint(cam_blueprint)

    # decoding cookie before each request
    app.before_request_funcs.setdefault(None, [decode_cookie])

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
