from flask import current_app
from datetime import datetime
from . import db


# Ensure this is at the top level, not nested inside any function
def update_reservation_status():
    with current_app.app_context():
        try:
            current_time = datetime.now()
            expired_reservations = Devices.query.filter(
                Devices.reservationEnd < current_time,
                Devices.reserved == True
            ).all()

            for device in expired_reservations:
                device.reserved = False

            db.session.commit()
        except Exception as e:
            current_app.logger.error('Failed to update reservations: %s', e)
