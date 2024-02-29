from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
import os
import logging

SCRIPTS_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"

class Config:
    SCHEDULER_API_ENABLED = True


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ksjxchalsikdjuhf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Initialize APScheduler
    app.config.from_object(Config())
    scheduler = APScheduler()
    scheduler.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Reservation

    with app.app_context():
        db.create_all()

    # Create folder for the log if it doesn't exist
    log_folder = os.path.join(os.path.dirname(SCRIPTS_FOLDER_PATH), "Log")
    if not os.path.exists(log_folder):
        os.mkdir(log_folder)

    # Configure the logging system for Werkzeug logs
    werkzeug_log_file = os.path.join(log_folder, "Werkzeug.log")
    werkzeug_logger = logging.getLogger('werkzeug')
    werkzeug_logger.setLevel(logging.INFO)

    werkzeug_file_handler = logging.FileHandler(werkzeug_log_file)
    werkzeug_file_handler.setLevel(logging.INFO)

    werkzeug_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    werkzeug_file_handler.setFormatter(werkzeug_formatter)

    werkzeug_logger.addHandler(werkzeug_file_handler)

    # Configure the logging system for custom logs
    custom_log_file = os.path.join(log_folder, "Inventory_tracking.log")
    custom_logger = logging.getLogger('custom')
    custom_logger.setLevel(logging.INFO)

    custom_file_handler = logging.FileHandler(custom_log_file)
    custom_file_handler.setLevel(logging.INFO)

    custom_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    custom_file_handler.setFormatter(custom_formatter)

    custom_logger.addHandler(custom_file_handler)

    # Log a custom message
    custom_logger.info(
        "----- Midmark Inventory Tracking System -----\n\n")
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def update_database():
        with app.app_context():
            try:
                current_time = datetime.now()
                # Query the Reservation table for expired reservations
                expired_reservations = Reservation.query.filter(
                    Reservation.end_time < current_time
                ).all()

                for reservation in expired_reservations:
                    db.session.delete(reservation)

                db.session.commit()
            except Exception as e:
                custom_logger.error(f'Failed to update reservations: {e}')


    with app.app_context():
        db.create_all()
        if not scheduler.get_job('your_job_id'):
            scheduler.add_job(id='your_job_id', func=update_database, trigger='interval', seconds=30)
        scheduler.start()

    return app