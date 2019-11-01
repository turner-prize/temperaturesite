from config import ma,db
from models import Temperature

class TemperatureSchema(ma.ModelSchema):
    class Meta:
        model = Temperature
        sqla_session = db.session