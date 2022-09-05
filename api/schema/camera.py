from api.service.database import ma
from api.model.camera import CameraModel


class CameraSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CameraModel
        include_relationships = True
        load_instance = True


camera_schema = CameraSchema()
cameras_schema = CameraSchema(many=True)