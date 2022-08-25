from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from sqlalchemy.sql import func

from api.service.database import db
from api.service.variables import USER_ROLES, ADMIN_ROLES


class UserModel(db.Model):
    """
    User Flask-SQLAlchemy Model

    Represents object contained in user table
    """
    __tablename__ = "user"
    # takes into account google/email authentication
    __table_args__ = (db.UniqueConstraint("google_id"), db.UniqueConstraint("email"))

    # An ID to use as a reference when sending email.
    external_id = db.Column(
        db.String, default=lambda: str(uuid.uuid4()), nullable=False
    )
    google_id = db.Column(db.String, nullable=True)
    activated = db.Column(db.Boolean, default=False, server_default="f", nullable=False)
    # if user sets up his account within the app
    _password = db.Column(db.String(100), nullable=False)

    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.Enum(*USER_ROLES, *ADMIN_ROLES), server_default="user")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    last_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return (
            f'**User**'
            f'id: {self.id}'
            f'created at: {self.created_at}'
            f'username: {self.username}'
            f'email: {self.email}'
            f'role: {self.role}'
            f'**User**'
        )

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)

