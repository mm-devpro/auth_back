from os import getenv
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import jwt
from sqlalchemy.sql import func

from api.service.database import db

SECRET_KEY = getenv('SECRET_KEY')


class UserModel(db.Model):
    """
    User Flask-SQLAlchemy Model

    Represents object contained in user table
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(255))

    def __repr__(self):
        return (
            f'**User**'
            f'id: {self.id}'
            f'created at: {self.created_at}'
            f'username: {self.username}'
            f'email: {self.email}'
            f'**User**'
        )

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key == 'password':
            self.__dict__['password'] = generate_password_hash(value)
            return

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :param user_id: id of current user to create token payload
        :return: string
        """
        try:
            payload = {
                'sub': user_id,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(days=30)
            }
            return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token: sent by the client
        :return: integer | string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'