from datetime import datetime
from config import db

class Temperature(db.Model):
    __tablename__ = 'temperature'
    temp = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    light = db.Column(db.Float)
    timestamp = db.Column(db.String, primary_key=True)
    device = db.Column(db.String)
    colour = db.Column(db.String)