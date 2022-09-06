from database import db


class CameraModel(db.Model):
    """
    Camera Flask-SQLAlchemy Model

    Represents object contained in camera table
    """
    __tablename__ = "camera"

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    source = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=False, server_default="0")
    locker_id = db.Column(db.Integer, db.ForeignKey('locker.id'), nullable=False)
