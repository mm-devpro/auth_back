from sqlalchemy.sql import func
from database import db


class AccountModel(db.Model):
    """
    Account Flask-SQLAlchemy Model

    Represents object contained in account table
    """
    __tablename__ = "account"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    users = db.relationship("User", back_populates='account')

    def __repr__(self):
        return f'<Account "{self.name}...">'
