from api.service.variables import LOCKER_TYPE

from api.service.database import db


class LockerModel(db.Model):
    """
    Locker Flask-SQLAlchemy Model

    Represents object contained in locker table
    """
    __tablename__ = "locker"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    access_lvl = db.Column(db.Enum([0, 1, 2, 3, 4, 5]), default=0, server_default="0")
    type = db.Column(db.Enum(*LOCKER_TYPE), server_default="door")
    # if user sets up his account within the app
    locked = db.Column(db.Boolean(), default=True, server_default="1")
    digit_activation = db.Column(db.Boolean(), server_default=True)
