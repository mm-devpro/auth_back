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