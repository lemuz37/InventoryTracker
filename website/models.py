from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    # User details
    admin = db.Column(db.Boolean, default=False)
    team = db.Column(db.String(150))
    project = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    user_name = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    # Relationships
    devices = db.relationship('Device', backref='user', lazy=True)
    reservations = db.relationship('Reservation', backref='user', lazy=True)

class Device(db.Model):
    __tablename__ = 'device_table'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key to link a device directly to a user upon checkout
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=True)
    reservation = db.relationship('Reservation', back_populates='device', uselist=False)
    # Device details
    device_category = db.Column(db.String(150))
    device_name = db.Column(db.String(150))
    model_number = db.Column(db.String(150))
    serial_number = db.Column(db.String(150))
    is_calibrated = db.Column(db.Boolean)
    calibration_start = db.Column(db.DateTime(timezone=True))
    calibration_end = db.Column(db.DateTime(timezone=True))
    owner = db.Column(db.String(150))
    project = db.Column(db.String(150))
    location = db.Column(db.String(150))
    checked_out = db.Column(db.Boolean, default=False, nullable=False)
    checkout_time = db.Column(db.DateTime(timezone=True))


class Reservation(db.Model):
    __tablename__ = 'reservation_table'

    id = db.Column(db.Integer, primary_key=True)
    # Reservation details
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    project = db.Column(db.String(150), nullable=True)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device_table.id'), nullable=False, unique=True)
    # Back reference from Device
    device = db.relationship('Device', back_populates='reservation', foreign_keys=[device_id])