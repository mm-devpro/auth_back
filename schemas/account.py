from database import ma
from models.account import AccountModel


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        include_relationships = True
        load_instance = True


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
