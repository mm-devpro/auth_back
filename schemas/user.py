from database import ma
from marshmallow import fields
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True
        load_instance = True
        exclude = ("_password",)

    password = fields.Str(required=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
