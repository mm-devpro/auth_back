from api.service.database import ma
from api.model.account_model import AccountModel


class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AccountModel
        include_relationships = True
        load_instance = True


account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)
