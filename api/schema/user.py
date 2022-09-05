from api.service.database import ma
from marshmallow import fields
from api.model.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True
        exclude = ("_password",)

    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
