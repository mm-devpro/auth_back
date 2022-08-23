from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init SQLAlchemy so we can use it later in our model
db = SQLAlchemy()
ma = Marshmallow()