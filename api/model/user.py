from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

from api.service.database import db
from api.service.variables import USER_ROLES, ADMIN_ROLES, USER_GROUP


class UserModel(db.Model):
    """
    User Flask-SQLAlchemy Model

    Represents object contained in user table
    """
    __tablename__ = "user"
    # takes into account google/email authentication
    __table_args__ = (db.UniqueConstraint("google_id"), db.UniqueConstraint("email"))

    # An ID to use as a reference when sending email.
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(100), nullable=True)
    activated = db.Column(db.Boolean, default=False, server_default="0", nullable=False)
    # if user sets up his account within the app
    _password = db.Column(db.String(500), nullable=False)

    username = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    surname = db.Column(db.String(255), nullable=True)
    digit_pwd = db.Column(db.Integer, default=0000, server_default="0000")
    access = db.Column(db.Integer, server_default="0")
    dob = db.Column(db.Date(), nullable=True)
    group = db.Column(db.Enum(*USER_GROUP), server_default="invite")
    email = db.Column(db.String(100), unique=True)
    img = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(*USER_ROLES, *ADMIN_ROLES), server_default="user")
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account = db.relationship('Account', back_populates='user')

    def __repr__(self):
        return f'<Account "{self.username}...">'

    @property
    def password(self):
        raise AttributeError("Can't read password")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self._password, password)
