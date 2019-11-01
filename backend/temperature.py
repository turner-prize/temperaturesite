from config import db
from models import Temperature
from schemas import TemperatureSchema

def read_all():
    
    d = Temperature.query.all()
    temperature_schema = TemperatureSchema(many=True)
    return temperature_schema.dump(d).data
    
def create(temperature):

    temp=temperature.get('temp')
    humidity=temperature.get('humidity')
    light=temperature.get('lightLevel')
    timestamp=temperature.get('timestamp')
    device=temperature.get('device')
    colour=temperature.get('colour')

    existing_record = Temperature.query \
        .filter(Temperature.timestamp == timestamp) \
        .one_or_none()

    # Can we insert this person?
    if existing_record is None:

        # Create a person instance using the schema and the passed-in person
        schema = TemperatureSchema()
        new_record = schema.load(temperature, session=db.session).data

        # Add the person to the database
        db.session.add(new_record)
        db.session.commit()

        # Serialize and return the newly created person in the response
        return schema.dump(new_record).data, 201

    # Otherwise, nope, person exists already
    else:
        abort(409, f'Record exists already')