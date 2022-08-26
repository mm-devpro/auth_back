from api.service.database import ma
from api.model.user import UserModel


class UserSchema(ma.Schema):
    class Meta:
        fields = ("email", "created_at", "username", "id")


user_schema = UserSchema()
users_schema = UserSchema(many=True)
