import email
from pytz import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(150))
    calibrated = db.Column(db.Boolean())
    serialNumber = db.Column(db.String(150))
    team = db.Column(db.String(150))
    project = db.Column(db.String(150))
    location = db.Column(db.String(150))
    calibrationStart = db.Column(db.DateTime(timezone=True))
    calibrationEnd = db.Column(db.DateTime(timezone=True))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_name = db.Column(db.String(150), db.ForeignKey('user.user_name'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_name = db.Column(db.String(150))
    admin = db.Column(db.Boolean())
    devices = db.relationship('Devices')