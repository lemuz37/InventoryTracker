from . import db
from flask_login import UserMixin


class Devices(db.Model):
    __tablename__ = "device_table"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(150))
    device_category = db.Column(db.String(150))
    device_name = db.Column(db.String(150))
    model_number = db.Column(db.String(150))
    serial_number = db.Column(db.String(150))
    calibrated = db.Column(db.Boolean())
    calibrationStart = db.Column(db.DateTime(timezone=True))
    calibrationEnd = db.Column(db.DateTime(timezone=True))
    team = db.Column(db.String(150))
    project = db.Column(db.String(150))
    location = db.Column(db.String(150))
    checkout_time = db.Column(db.DateTime(timezone=True))


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean())
    team = db.Column(db.String(150))
    project = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    last_activity = db.Column(db.DateTime(timezone=True))
