from database import ma
from models.locker import LockerModel


class LockerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LockerModel
        include_relationships = True
        load_instance = True


locker_schema = LockerSchema()
lockers_schema = LockerSchema(many=True)
