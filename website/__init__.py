from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import logging

SCRIPTS_FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ksjxchalsikdjuhf'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Devices

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

    return app
