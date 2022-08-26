from api.service.database import ma
from marshmallow_sqlalchemy import auto_field
from marshmallow import fields
from api.model.user import UserModel
from api.service.variables import USER_ROLES, ADMIN_ROLES


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True
        exclude = ("_password",)

    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
